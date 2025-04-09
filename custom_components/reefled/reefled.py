import logging
import threading

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    DEFAULT_PULL_RATE
    )

_LOGGER = logging.getLogger(__name__)

class ReefLed(threading.Thread):

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._entry = entry
        _LOGGER.error(entry)

