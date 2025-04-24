""" Implements the sensor entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    DAILY_PROG_INTERNAL_NAME,
    )

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchDeviceClass,
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
    entities += [DailyProgSwitchEntity(coordinator, entry)]
    async_add_entities(entities, True)



class DailyProgSwitchEntity(CoordinatorEntity,SwitchEntity):
    """La classe de l'entité Sensor"""

    def __init__(
        self,
            coordinator,
            entry_infos, 
    ) -> None:
        """Initisalisation de notre entité"""
        super().__init__(coordinator,context=DAILY_PROG_INTERNAL_NAME)
        self._attr_name = entry_infos.title+"_"+DAILY_PROG_INTERNAL_NAME
        self._attr_unique_id = entry_infos.title+"_"+DAILY_PROG_INTERNAL_NAME
        self.coordinator = coordinator
        self._attr_device_class=SwitchDeviceClass.SWITCH
        self._state = False
        
    @property
    def icon(self):
        """Return device icon for this entity."""
        return "mdi:calendar-range"

    @callback
    def _handle_coordinator_update(self) -> None:
        self._state= self.coordinator.daily_prog
        self.async_write_ha_state()
        

    @property
    def is_on(self):
        return self._state


    def turn_on(self,**kwargs) -> None:
        self._state=True

    def turn_off(self,**kwargs) -> None:
        self._state=False
