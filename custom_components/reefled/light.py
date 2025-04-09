""" Implements the light entity """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import LightEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):
    """Configuration de la plate-forme  à partir de la configuration
    trouvée dans configuration.yaml"""

    pass
    # _LOGGER.error("*** --- *** Calling async_setup_platform entry=%s", entry)

    # entities=[]
    # entities[0]= LEDEntity(hass, "white")
    # entities[0]= LEDEntity(hass, "blue")
    # entities[0]= LEDEntity(hass, "")
    # async_add_entities(entities, True)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument                                                                                                                                                                                 
):
    """Configuration de la plate-forme tuto_hacs à partir de la configuration                                                                                                                                                               
    trouvée dans configuration.yaml"""

    _LOGGER.error("*** --- *** Calling async_setup_entry entry=%s", entry)
    entities=[]
    entities += [LEDEntity(hass, entry, "white")]
    entities += [LEDEntity(hass, entry, "blue")]
    entities += [LEDEntity(hass, entry, "moon")]
    async_add_entities(entities, True)
    
class LEDEntity(LightEntity):
    """La classe de l'entité LED"""

    def __init__(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
            device,
            color,  # pylint: disable=unused-argument
    ) -> None:
        _LOGGER.error("-- LEDEntity -- %s"%color)
        """Initisalisation de notre entité"""
        self._attr_name = color
        self._attr_unique_id = device.title+'_'+color
