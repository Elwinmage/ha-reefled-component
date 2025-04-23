""" Implements the sensor entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    STATUS_INTERNAL_NAME
    )

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorDeviceClass,
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
    entities += [GlobalStateBinarySensorEntity(coordinator, entry)]
    async_add_entities(entities, True)



class GlobalStateBinarySensorEntity(CoordinatorEntity,BinarySensorEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
            coordinator,
            entry_infos, 
    ) -> None:
        """Initisalisation de notre entité"""
        super().__init__(coordinator,context=STATUS_INTERNAL_NAME)
        self._attr_name = entry_infos.title+"_"+STATUS_INTERNAL_NAME
        self._attr_unique_id = entry_infos.title+"_"+STATUS_INTERNAL_NAME
        self.coordinator = coordinator
        self._attr_device_class = BinarySensorDeviceClass.LIGHT
        self._state = False
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:wall-sconce-flat"

    @callback
    def _handle_coordinator_update(self) -> None:
        self._state= self.coordinator.data[STATUS_INTERNAL_NAME]

        self.async_write_ha_state()
        

    @property
    def is_on(self):
        return self._state
