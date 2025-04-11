import logging
import asyncio
import functools
import threading
import time

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

from .const import (
    DOMAIN,
    PLATFORMS,
    CONFIG_FLOW_IP_ADDRESS
    )

from .reefled import ReefLed

import traceback

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the ReefLed component."""
    # hass.data[DOMAIN] stores one entry for each ReefLed instance using ip address as a key
    hass.data.setdefault(DOMAIN, {})

    # Callback function to start polling when HA starts
    def start_polling(event):
        _LOGGER.debug("Start polling components...")
        for component in hass.data[DOMAIN].values():
            _LOGGER.debug("* %s"%component)
            if not component.is_alive():
                component.start_polling()

    # Callback function to stop polling when HA stops
    def stop_polling(event):
        for component in hass.data[DOMAIN].values():
            if component.is_alive():
                component.stop_polling()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_polling)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_polling)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Creation des entités à partir d'une configEntry"""

    _LOGGER.debug(
        "Appel de async_setup_entry entry: entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    coordinator = ReefLed(hass, entry)

    coordinator.start_polling()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
