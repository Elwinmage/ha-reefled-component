""" Implements the sensor entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo


from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    FAN_INTERNAL_NAME,
    TEMPERATURE_INTERNAL_NAME,
    IP_INTERNAL_NAME,
    DAYS,
    )

from homeassistant.components.sensor import (
     SensorDeviceClass,
     SensorEntity,
     SensorStateClass,
 )

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .coordinator import ReefLedCoordinator


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

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities=[]
    entities += [FanSensorEntity(coordinator, entry)]
    entities += [TemperatureSensorEntity(coordinator, entry)]
    entities += [IPSensorEntity(coordinator, entry)]
    for i in range(1,8):
        entities += [AutoSensorEntity(coordinator,entry,i)]
    async_add_entities(entities, True)


class AutoSensorEntity(CoordinatorEntity,SensorEntity):
    """ Schedule """
    def __init__(
            self,
            coordinator,
            entry_infos,
            idx
            ) -> None:
        super().__init__(coordinator,context=idx)
        self._idx = 'auto_'+str(idx)
        self._attr_name=entry_infos.title+'_'+DAYS[idx-1]
        self._attr_unique_id=entry_infos.title+'_'+self._idx
        self.coordinator=coordinator

    @property
    def icon(self):
        return "mdi:calendar"
    
    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data[self._idx]
        self._attr_native_value=data['name']
        _LOGGER.debug("*/*/*/__handle_coordinator_update%s"%data)
        self._attr_extra_state_attributes = {'data': data['data'],'clouds':data['clouds']}
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.coordinator.device_info


        
class FanSensorEntity(CoordinatorEntity,SensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
            coordinator,
            entry_infos, 
    ) -> None:
        """Initisalisation de notre entité"""
        super().__init__(coordinator,context=FAN_INTERNAL_NAME)
        self._attr_name = entry_infos.title+"_"+FAN_INTERNAL_NAME
        self._attr_unique_id = entry_infos.title+"_"+FAN_INTERNAL_NAME
        self.coordinator = coordinator
        self._attr_device_class = SensorDeviceClass.POWER_FACTOR
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement="%"
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:fan"

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value= self.coordinator.data[FAN_INTERNAL_NAME]
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.coordinator.device_info
        

class TemperatureSensorEntity(CoordinatorEntity,SensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
            coordinator,
        entry_infos,  # pylint: disable=unused-argument
    ) -> None:
        super().__init__(coordinator,context=TEMPERATURE_INTERNAL_NAME)
        """Initisalisation de notre entité"""
        self._attr_name = entry_infos.title+"_"+TEMPERATURE_INTERNAL_NAME
        self._attr_unique_id = entry_infos.title+'_'+TEMPERATURE_INTERNAL_NAME
        self.coordinator = coordinator
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:thermometer"

    @callback
    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug("UPDATE Temperature")
        self._attr_native_value= self.coordinator.data[TEMPERATURE_INTERNAL_NAME]
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.coordinator.device_info
   

class IPSensorEntity(CoordinatorEntity,SensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
            coordinator,
        entry_infos,  # pylint: disable=unused-argument
    ) -> None:
        super().__init__(coordinator,context=IP_INTERNAL_NAME)
        """Initisalisation de notre entité"""
        self._attr_name = entry_infos.title+"_"+IP_INTERNAL_NAME
        self._attr_unique_id = entry_infos.title+'_'+IP_INTERNAL_NAME
        self.coordinator = coordinator
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:check-network-outline"

    @callback
    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug("UPDATE Ip")
        self._attr_native_value= self.coordinator.data[IP_INTERNAL_NAME]
        self.async_write_ha_state()
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.coordinator.device_info
