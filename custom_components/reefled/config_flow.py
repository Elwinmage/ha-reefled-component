"""Config flow for Reefled component."""

import voluptuous as vol
import glob
import logging

from functools import partial

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
)

_LOGGER = logging.getLogger(__name__)

class ReefLedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ReefLed config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def _title(self, user_input):
        f_kwargs = {}
        f_kwargs["ip"] = user_input[CONFIG_FLOW_IP_ADDRESS]
        fname=await self.hass.async_add_executor_job(partial(get_friendly_name,**f_kwargs))
        return fname    

    async def _unique_id(self, user_input):
        f_kwargs = {}
        f_kwargs["ip"] = user_input[CONFIG_FLOW_IP_ADDRESS]
        uuid=await self.hass.async_add_executor_job(partial(get_unique_id,**f_kwargs))
        return uuid

    async def async_step_import(self, user_input=None):
        """Create a new entity from configuration.yaml import."""
        pass
        # _LOGGER.error("**** user_input **** %"%user_input)
        # config_entry =  await self.async_set_unique_id(self._unique_id(user_input))
        # # Remove entry (from storage) matching the same unique id
        # if config_entry:
        #     self.hass.config_entries.async_remove(config_entry.entry_id)

        # return self.async_create_entry(
        #     title=self._title(user_input),
        #     data=user_input,
        # )


    async def async_step_user(self, user_input=None):
        """Create a new entity from UI."""
        if user_input is not None:
            #Identify device with unique ID
            uuid = await self._unique_id(user_input)
            _LOGGER.debug("-- ** UUID ** -- %s"%uuid)
            #await self.async_set_unique_id(uuid)
            await self.async_set_unique_id(str(uuid))
            self._abort_if_unique_id_configured()
            title=await self._title(user_input)
            _LOGGER.debug("-- ** TITLE ** -- %s"%title)
            return self.async_create_entry(
                title=title,
                data=user_input,
            )
            
        detected_devices = await self.hass.async_add_executor_job(get_reefleds)
        _LOGGER.info(detected_devices)
        if len(detected_devices) > 0 :
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
