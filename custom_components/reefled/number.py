import asyncio
import functools
import logging

import voluptuous as vol

from homeassistant.components.number import PLATFORM_SCHEMA, Number
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from . import async_get_or_create
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry_infos, async_add_entities):
    """Set up a MCP23017 binary_sensorReefLed Color value  entry."""
     _LOGGER.debug("async_setup")
      entity = ReefLedNumber(hass, entry_infos)
      async_add_entities([entity], True)
      platform = async_get_current_platform()
      await async_get_or_create(hass, entity)

class ReefLedNumber(Number):
    """Represent a led color value."""
    pass
