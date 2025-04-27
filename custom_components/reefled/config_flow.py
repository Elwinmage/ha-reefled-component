"""Config flow for Reefled component."""

import voluptuous as vol
import glob
import logging

from functools import partial
from time import time

from homeassistant import config_entries
from homeassistant.core import callback

from .auto_detect import (
    get_reefleds,
    get_unique_id,
    get_friendly_name
)

from .const import (
    PLATFORMS,
    DOMAIN,
    CONFIG_FLOW_IP_ADDRESS,
    VIRTUAL_LED,
)

_LOGGER = logging.getLogger(__name__)

class ReefLedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ReefLed config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def _title(self, user_input):
        fname=user_input[CONFIG_FLOW_IP_ADDRESS].split(' ')[1]
        return fname    

    async def _unique_id(self, user_input):
        f_kwargs = {}
        f_kwargs["ip"] = user_input[CONFIG_FLOW_IP_ADDRESS].split(' ')[0]
        uuid=await self.hass.async_add_executor_job(partial(get_unique_id,**f_kwargs))
        return uuid

    async def async_step_user(self, user_input=None):
        """Create a new entity from UI."""
        if user_input is not None:
            if user_input[CONFIG_FLOW_IP_ADDRESS] == VIRTUAL_LED:
                title=VIRTUAL_LED+'-'+str(int(time()))
                user_input[CONFIG_FLOW_IP_ADDRESS]=title
                _LOGGER.debug("-- ** UUID ** -- %s"%title)
                await self.async_set_unique_id(title)
            else:
                #Identify device with unique ID
                uuid = await self._unique_id(user_input)
                _LOGGER.info("-- ** UUID ** -- %s"%uuid)
                #await self.async_set_unique_id(uuid)
                await self.async_set_unique_id(str(uuid))
                self._abort_if_unique_id_configured()
                title=await self._title(user_input)
                _LOGGER.info("-- ** TITLE ** -- %s"%title)
                user_input[CONFIG_FLOW_IP_ADDRESS]=user_input[CONFIG_FLOW_IP_ADDRESS].split(' ')[0]
    
            return self.async_create_entry(
                title=title,
                data=user_input,
            )
            
        detected_devices = await self.hass.async_add_executor_job(get_reefleds)
        _LOGGER.info("Detected devices: %s"%detected_devices)
        if DOMAIN in self.hass.data:
            for device in self.hass.data[DOMAIN]:
                coordinator=self.hass.data[DOMAIN][device]
                if type(coordinator).__name__=='ReefLedCoordinator' and coordinator.detected_id in detected_devices:
                    _LOGGER.info("%s skipped (already configured)"%coordinator.detected_id)
                    detected_devices.remove(coordinator.detected_id)
        _LOGGER.info("Available devices: %s"%detected_devices)
        detected_devices += [VIRTUAL_LED]
        if len(detected_devices) > 1 :
            return self.async_show_form(
                step_id="user",
                 data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONFIG_FLOW_IP_ADDRESS
                        ): vol.In(detected_devices),
                    }
                     ),
                )

        else:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONFIG_FLOW_IP_ADDRESS
                        ): str,
                    }
                ),
            )
