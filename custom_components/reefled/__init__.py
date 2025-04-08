import logging
import asyncio
import functools
import threading
import time

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
from .const import DOMAIN, PLATFORMS, CONFIG_FLOW_IP_ADDRESS

import traceback

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "number"]
REEFLED_DATA_LOC=asyncio.Lock()

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the ReefLed component."""
    _LOGGER.debug("async_setup")
    # hass.data[DOMAIN] stores one entry for each ReefLed instance using ip address as a key
    hass.data.setdefault(DOMAIN, {})

    # Callback function to start polling when HA starts
    def start_polling(event):
        for component in hass.data[DOMAIN].values():
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

    hass.data.setdefault(DOMAIN, {})
    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, config_entry):
    """Unload REEFLED switch entry corresponding to config_entry."""
    component = hass.data[DOMAIN][config_entry.data[CONFIG_FLOW_IP_ADDRESS]]
    component.reInit()

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Fonction qui force le rechargement des entités associées à une configEntry"""
    component = hass.data[DOMAIN][entry.data[CONFIG_FLOW_IP_ADDRESS]]
    component.reInit()
    await hass.config_entries.async_reload(entry.entry_id)

async def async_get_or_create(hass, entity):
    """Get or create a REEFLED component from entity bus and i2c address."""
    ip_address = entity.address
    # DOMAIN data async mutex
    try:
        async with REEFLED_DATA_LOCK:
            if ip_address in hass.data[DOMAIN]:
                component = hass.data[DOMAIN][ip_address]
            else:
                # Try to create component when it doesn't exist
                component = await hass.async_add_executor_job(
                    functools.partial(REEFLED, hass,ip_address)
                )
                hass.data[DOMAIN][ip_address] = component

                # Start polling thread if hass is already running
                if hass.is_running:
                    component.start_polling()

                devices = device_registry.async_get(hass)
                devices.async_get_or_create(
                    config_entry_id=entity._entry_infos.entry_id,
                    identifiers={(DOMAIN, ip_address)},
                    manufacturer=DEVICE_MANUFACTURER,
                    model=DOMAIN,
                    name=f"{DOMAIN}@{ip_address}",
                )

            # Link entity to component
            await hass.async_add_executor_job(
                functools.partial(component.register_entity, entity)
            )
    except ValueError as error:
        component = None
        await hass.config_entries.async_remove(entity._entry_infos.entry_id)

        hass.components.persistent_notification.create(
            f"Error: Unable to access {DOMAIN}{ip_address} ({error})",
            title=f"{DOMAIN} Configuration",
            notification_id=f"{DOMAIN} notification",
        )

    return component



class REEFLED(threading.Thread):
    """REEFLED component (device)"""

    def __init__(self, hass,address):
        # Address is this form /dev/i2c-1@0x48
        self._hass     = hass
        self._address  = address
        self._entities = [None for i in range(3)]
        self._device_lock = threading.Lock()
        self._run = False
        
        threading.Thread.__init__(self, name=self.unique_id)
        _LOGGER.info("%s device created", self.unique_id)

    def __enter__(self):
        """Lock access to device (with statement)."""
        self._device_lock.acquire()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Unlock access to device (with statement)."""
        self._device_lock.release()
        return False

    def reInit(self):
        self._to_init = True
    
    @property
    def unique_id(self):
        """Return component unique id."""
        return f"{DOMAIN}{self._address}"


    @property
    def address(self):
        """Return ip address"""
        return self._address

    def start_polling(self):
        """Start polling thread."""
        self._run = True
        self.start()

    def stop_polling(self):
        """Stop polling thread."""
        self._run = False
        self.join()

    def run(self):
        """Poll all ports once and call corresponding callback if a change is detected."""
        _LOGGER.info("%s start polling thread", self.unique_id)
        while True:
            _LOGGER.info("*", self.unique_id)
            time.sleep(DEFAULT_PULL_RATE)
            
    def register_entity(self, entity):
        """Register entity to this device instance."""
        return True
    

