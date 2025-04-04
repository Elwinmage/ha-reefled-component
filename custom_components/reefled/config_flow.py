"""Config flow for MCP23017 component."""

import voluptuous as vol
import glob
import logging

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
)

PLATFORMS = ["sensor","number"]

_LOGGER = logging.getLogger(__name__)


class ReefLedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ReefLed config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _title(self, user_input):
        return "%s" % (
            user_input[CONFIG_FLOW_IP_ADDRESS],
        )

    def _unique_id(self, user_input):
        return "%s.%s" % (
            DOMAIN,
            user_input[CONF_FLOW_IP_ADDRESS],
        )

    async def async_step_import(self, user_input=None):
        """Create a new entity from configuration.yaml import."""

        config_entry =  await self.async_set_unique_id(self._unique_id(user_input))
        # Remove entry (from storage) matching the same unique id
        if config_entry:
            self.hass.config_entries.async_remove(config_entry.entry_id)

        return self.async_create_entry(
            title=self._title(user_input),
            data=user_input,
        )


    async def async_step_user(self, user_input=None):
        """Create a new entity from UI."""

        if user_input is not None:
            await self.async_set_unique_id(self._unique_id(user_input))
            self._abort_if_unique_id_configured()

            if CONFIG_FLOW_IP_ADDRESS not in user_input:
                user_input[CONF_FLOW_PIN_NAME] = "%s" % (
                    user_input[CONFIG_FLOW_IP_ADDRESS],
                )
            
            return self.async_create_entry(
                title=self._title(user_input),
                data=user_input,
            )
        detected_devices=[]       

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONFIG_FLOW_IP_ADDRESS
                    ): vol.In(detected_devices),
                    vol.Required(
                        CONFIG_FLOW_IP_ADDRESS
                    ): str,
                }
            ),
        )
