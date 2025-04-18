import logging

from datetime import  datetime,timedelta

from homeassistant.core import HomeAssistant

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from typing import Any

from .const import (
    DOMAIN,
    SCAN_INTERVAL)

from .reefled import ReefLedAPI

_LOGGER = logging.getLogger(__name__)

class ReefLedCoordinator(DataUpdateCoordinator[dict[str,Any]]):

    def __init__(
            self,
            hass: HomeAssistant,
            ip
    ) -> None:
        """Initialize coordinator."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL))
        _LOGGER.debug("**** ** ***** %s"%ip)
        self.my_api = ReefLedAPI(ip)
        
    async def _async_setup(self) -> None:
        """Do initialization logic."""
        return await self.my_api.get_initial_data()
        
    async def _async_update_data(self) -> dict[str,Any]:
        """Do the usual update"""
        return await self.my_api.update()
    
    async def async_send_new_values(self):
        return await self.my_api.async_send_new_values()

    async def async_config_entry_first_refresh(self):
        return await self.my_api.async_first_refresh()
