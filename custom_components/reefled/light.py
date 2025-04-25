""" Implements the light entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS

from homeassistant.core import callback
        
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
        

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .coordinator import ReefLedCoordinator

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    CONFIG_FLOW_IP_ADDRESS,
    WHITE_INTERNAL_NAME,
    BLUE_INTERNAL_NAME,
    MOON_INTERNAL_NAME,
)

async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    """Configuration de la plate-forme  à partir de la configuration
    trouvée dans configuration.yaml"""

    pass

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None, 
):

    _LOGGER.debug("Reefled.light.async_setup_entry.config_entry %s"%config_entry)
    _LOGGER.debug("DOMAIN: %s, entry_id: %s"%(DOMAIN, config_entry.entry_id))

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    #await coordinator.async_config_entry_first_refresh()
    async_add_entities(
        [LEDEntity(coordinator, config_entry, MOON_INTERNAL_NAME,'mdi:lightbulb-night-outline'),
         LEDEntity(coordinator, config_entry, WHITE_INTERNAL_NAME,'mdi:lightbulb-outline'),
         LEDEntity(coordinator, config_entry, BLUE_INTERNAL_NAME)], True
    )


    """Configuration de la plate-forme tuto_hacs à partir de la configuration"""
    
    
class LEDEntity(CoordinatorEntity, LightEntity):
    """La classe de l'entité LED"""


    def __init__(self, coordinator, device,idx,icon="mdi:lightbulb"):
        """Pass coordinator to CoordinatorEntity."""
        _LOGGER.debug("Reefled.light.__init__")
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self._icon = icon
        self._attr_supported_color_modes = [ColorMode.BRIGHTNESS]
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._state = "off"
        self._brightness = 0
        self.coordinator=coordinator
        self._attr_name=device.title+'_'+idx
        self._attr_unique_id=device.title+'_'+idx
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Reefled.light.__handle_coordinator_update")        
        _LOGGER.debug("%s --> %s"%(self.idx,self.coordinator.data[self.idx]))
        self._brightness =  self.coordinator.data[self.idx]
        if self.brightness > 0:
            self._state='on'
        else:
            self._state='off'
        self.async_write_ha_state()
        

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        _LOGGER.debug("Reefled.light.async_turn_on %s"%kwargs)
        if ATTR_BRIGHTNESS in kwargs:
            ha_value = int(kwargs[ATTR_BRIGHTNESS])
            self.coordinator.data[self.idx]=ha_value
            await self.coordinator.async_send_new_values()
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        self._brightness=0
        self._state="off"
        self.coordinator.data[self.idx]=0
        await self.coordinator.async_send_new_values()
        await self.coordinator.async_request_refresh()
        
            
    @property
    def icon(self):
        return self._icon
        
    @property
    def brightness(self) -> int:
        """Return the current brightness."""
        return self._brightness
    
    @property
    def is_on(self):
        return self.brightness > 0

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.coordinator.device_info
    
