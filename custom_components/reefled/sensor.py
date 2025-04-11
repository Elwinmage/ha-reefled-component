""" Implements the sensor entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    FAN_INTERNAL_NAME,
    TEMPERATURE_INTERNAL_NAME
    )

from homeassistant.components.sensor import (
     SensorDeviceClass,
     SensorEntity,
     SensorStateClass,
 )

async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):
    """Configuration de la plate-forme à partir de la configuration
    trouvée dans configuration.yaml"""
    pass

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):
    """Configuration de la plate-forme tuto_hacs à partir de la configuration graphique"""

    _LOGGER.debug("*** --- *** Calling async_setup_entry entry=%s", entry)
    entities=[]
    entities += [FanSensorEntity(hass, entry)]
    entities += [TemperatureSensorEntity(hass, entry)]
    async_add_entities(entities, True)



class FanSensorEntity(SensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
        hass: HomeAssistant,  
        entry_infos, 
    ) -> None:
        """Initisalisation de notre entité"""
        self._attr_name = "Fan"
        self._attr_unique_id = entry_infos.title+'_Fan'
        self._hass = hass
        self._component= hass.data[DOMAIN][entry_infos.entry_id]
        self._attr_device_class = SensorDeviceClass.POWER_FACTOR
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement="%"
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:fan"

    def update(self) -> None:
        self._attr_native_value = self._component.get_value(FAN_INTERNAL_NAME)

        

class TemperatureSensorEntity(SensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        entry_infos,  # pylint: disable=unused-argument
    ) -> None:
        """Initisalisation de notre entité"""
        self._attr_name = "temperature"
        self._attr_unique_id = entry_infos.title+'_Temperature'
        self._hass = hass
        self._component= hass.data[DOMAIN][entry_infos.entry_id]
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:thermometer"

    def update(self) -> None:
        _LOGGER.debug("UPDATE Temperature")
        self._attr_native_value= self._component.get_value(TEMPERATURE_INTERNAL_NAME)

    
