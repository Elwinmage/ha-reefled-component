""" Implements the light entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS

from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    WHITE_INTERNAL_NAME,
    BLUE_INTERNAL_NAME,
    MOON_INTERNAL_NAME
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
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None, 
):
    """Configuration de la plate-forme tuto_hacs à partir de la configuration"""
    
    entities=[]
    entities += [LEDEntity(hass, entry, WHITE_INTERNAL_NAME,icon="mdi:lightbulb-outline")]
    entities += [LEDEntity(hass, entry, BLUE_INTERNAL_NAME)]
    entities += [LEDEntity(hass, entry,MOON_INTERNAL_NAME,icon="mdi:lightbulb-night-outline")]
    async_add_entities(entities, True)
    
class LEDEntity(LightEntity):
    """La classe de l'entité LED"""

    def __init__(
        self,
        hass: HomeAssistant, 
            device,
            color, 
            icon = "mdi:lightbulb"
    ) -> None:
        """Initisalisation de notre entité"""
        self._hass = hass
        self._device = device
        self._component = hass.data[DOMAIN][device.entry_id]
        self._attr_name = color
        self._icon = icon
        self._attr_unique_id = device.title+'_'+color
        self._attr_supported_color_modes = [ColorMode.BRIGHTNESS]
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._state = "off"
        self._brightness = 0

    def update(self) -> None:
        self._brightness = self._component.get_value(self.name)
        _LOGGER.debug("Update %s %s"%(self.name,self.brightness))
        if self.brightness > 0:
            self._state = 'on'
        else:
            self._state="off"

    @property
    def brightness(self) -> int:
        """Return the current brightness."""
        return self._brightness

    async def async_turn_on(self, **kwargs) -> None:
            """Turn device on."""
            _LOGGER.debug(kwargs)
            if ATTR_BRIGHTNESS in kwargs:
                ha_value = int(kwargs[ATTR_BRIGHTNESS])
                hw_value = int(ha_value/255*100)
                _LOGGER.debug("set value to %d -> %d for %s"%(ha_value,hw_value,self._attr_name))
                self._component.set_value(self.name,ha_value)
            else:
                self._component.set_value(self.name,255)

    async def async_turn_off(self,**kwargs) -> None:
        self._component.set_value(self.name,0)
        
    @property
    def  icon(self):
        """Return  device icon"""
        return self._icon
    
    @property
    def is_on(self):
        return self._brightness > 0
        
        

    
