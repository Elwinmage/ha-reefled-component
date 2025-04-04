"""Platform for mcp23017-based binary_sensor."""

import asyncio
import functools
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from . import async_get_or_create
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)

from .const import (
    CONF_FLOW_PIN_NAME,
    CONF_FLOW_PIN_NUMBER,
    CONF_FLOW_PLATFORM,
    CONF_I2C_ADDRESS,
    CONF_INVERT_LOGIC,
    CONF_PINS,
    CONF_PULL_MODE,
    DEFAULT_I2C_ADDRESS,
    DEFAULT_INVERT_LOGIC,
    DEFAULT_PULL_MODE,
    DOMAIN,
    MODE_DOWN,
    MODE_UP,
    DEVICE_MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)

_PIN_SCHEMA = vol.Schema({cv.positive_int: cv.string})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PINS): _PIN_SCHEMA,
        vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
        vol.Optional(CONF_PULL_MODE, default=DEFAULT_PULL_MODE): vol.All(
            vol.Upper, vol.In([MODE_UP, MODE_DOWN])
        ),
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    }
)

async def async_setup_entry(hass, entry_infos, async_add_entities):
    """Set up a MCP23017 binary_sensor entry."""
    if(entry_infos.data[CONF_FLOW_PLATFORM])=='binary_sensor':
        entity = MCP23017BinarySensor(hass, entry_infos)
        async_add_entities([entity], True)
        platform = async_get_current_platform()
        await async_get_or_create(hass, entity)

class MCP23017BinarySensor(BinarySensorEntity):
    """Represent a binary sensor that uses MCP23017."""

    def __init__(self, hass, entry_infos):
        """Initialize the MCP23017 binary sensor."""
        self._state = False
        self._hass = hass
        self._entry_infos = entry_infos
        self._i2c_address = entry_infos.data[CONF_I2C_ADDRESS]
        self._pin_name = entry_infos.data[CONF_FLOW_PIN_NAME]
        self._pin_number = entry_infos.data[CONF_FLOW_PIN_NUMBER]
        # Get invert_logic from config flow (options) or import (data)
        self._invert_logic = entry_infos.options.get(
            CONF_INVERT_LOGIC,
            entry_infos.data.get(
                CONF_INVERT_LOGIC,
                DEFAULT_INVERT_LOGIC
            )
        )
        # Get pull_mode from config flow (options) or import (data)
        self._pullup = entry_infos.options.get(
            CONF_PULL_MODE,
            entry_infos.data.get(
                CONF_PULL_MODE,
                DEFAULT_PULL_MODE
            )
        )

        #Subscribe to updates of config entry options
        self._unsubscribe_update_listener = entry_infos.add_update_listener(
           self.async_config_update
        )
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:radiobox-blank"

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return f"{self._i2c_address}-{self._pin_number:02x}"

    @property
    def should_poll(self):
        """No polling needed from homeassistant for this entity."""
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return self._pin_name

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self._state

    @property
    def pin(self):
        """Return the pin number of the entity."""
        return self._pin_number

    @property
    def address(self):
        """Return the i2c address of the entity."""
        return self._i2c_address

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN,self.address)},
            name=self.address,
            manufacturer=DEVICE_MANUFACTURER,
            model=DOMAIN,
        )

    def set_state(self,state):
        self._state = state
    
    @property
    def device(self):
        """Get device property."""
        return self._device

    @device.setter
    def device(self, value):
        """Set device property."""
        self._device = value

    @callback
    async def async_push_update(self, state):
        """Update the GPIO state."""
        self._state = state
        self.async_schedule_update_ha_state()

    @callback
    async def async_config_update(self, hass, entry_infos):
        """Handle update from config entry options."""
        _LOGGER.debug("[%s] async_config_update"%(self.unique_id))
        old_logic = self._invert_logic 
        self._invert_logic = entry_infos.options[CONF_INVERT_LOGIC]
        if old_logic != self._invert_logic:
            self._state = False
            _LOGGER.debug("[%s] New invert logic value set: %s"%(self.unique_id,self._invert_logic ))
        self._pullup = entry_infos.options[CONF_PULL_MODE]
        self.async_schedule_update_ha_state()
    
    def unsubscribe_update_listener(self):
        """Remove listener from config entry options."""
        self._unsubscribe_update_listener()

    async def async_unload_entry(hass, config_entry):
        """Unload MCP23017 binary entry corresponding to config_entry."""
        _LOGGER.warning("[FIXME] async_unload_entry not implemented")
