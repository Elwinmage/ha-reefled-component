import logging
import asyncio

from datetime import  datetime,timedelta

from homeassistant.core import HomeAssistant

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from typing import Any

from .const import (
    DOMAIN,
    CONFIG_FLOW_IP_ADDRESS,
    SCAN_INTERVAL,
    MODEL_NAME,
    MODEL_ID,
    HW_VERSION,
    SW_VERSION,
    DEVICE_MANUFACTURER,
)

from .reefled import ReefLedAPI

_LOGGER = logging.getLogger(__name__)

class ReefLedCoordinator(DataUpdateCoordinator[dict[str,Any]]):

    def __init__(
            self,
            hass: HomeAssistant,
            entry
    ) -> None:
        """Initialize coordinator."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL))
        self._ip = entry.data[CONFIG_FLOW_IP_ADDRESS]
        self.my_api = ReefLedAPI(self._ip)
        self._title = entry.title
        _LOGGER.debug("**** ** ***** %s"%self._ip)
        
        
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

    def daily_prog(self):
        return self.my_api.daily_prog


    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.model_id)
            },
            name=self.title,
            manufacturer=DEVICE_MANUFACTURER,
            model=self.model,
            model_id=self.model_id,
            hw_version=self.hw_version,
            sw_version=self.sw_version,
#            via_device=(DOMAIN, self.title),
        )
        
    
    @property
    def title(self):
        return self._title

    @property
    def model(self):
        return self.my_api.data[MODEL_NAME]

    @property
    def model_id(self):
        return self.my_api.data[MODEL_ID]

    @property
    def hw_version(self):
        return self.my_api.data[HW_VERSION]


    @property
    def sw_version(self):
        return self.my_api.data[SW_VERSION]


class ReefLedVirtualCoordinator(DataUpdateCoordinator[dict[str,Any]]):

    def __init__(
            self,
            hass: HomeAssistant,
            entry
    ) -> None:
        """Initialize coordinator."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL))
        self._title=entry.title
        self._slaves = []
        self.data = {}
        _LOGGER.debug(hass.data[DOMAIN])
        for l in  hass.data[DOMAIN]:
            led = hass.data[DOMAIN][l]
            if type(led).__name__=='ReefLedVirtualCoordinator':
                _LOGGER.debug("Virtual LED: %s"%l)
            else:
                _LOGGER.debug("LED: %s"%l)
                self._slaves += [led]
        
    async def _async_setup(self) -> None:
        """Do initialization logic."""
        pass
        
    async def _async_update_data(self) -> dict[str,Any]:
        """Do the usual update"""
        pass
    
    async def async_send_new_values(self):
        pass

    async def async_config_entry_first_refresh(self):
        pass

    def daily_prog(self):
        pass

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.title)
            },
            name=self.title,
            manufacturer=DEVICE_MANUFACTURER,
#            via_device=(DOMAIN, self.title),
        )
        
        
    @property
    def title(self):
        return self._title
    
    @property
    def slaves(self):
        return self._slaves
