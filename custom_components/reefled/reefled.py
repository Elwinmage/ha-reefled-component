import logging
import json
import time
import asyncio

import datetime

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import requests

from .const import (
    DOMAIN,
    CONFIG_FLOW_IP_ADDRESS,
    FAN_INTERNAL_NAME,
    TEMPERATURE_INTERNAL_NAME,
    WHITE_INTERNAL_NAME,
    BLUE_INTERNAL_NAME,
    MOON_INTERNAL_NAME,
    CONVERSION_COEF
)

_LOGGER = logging.getLogger(__name__)

#API
# /
# /dashboard
# /acclimation
# /device-info
# /moonphase
# /current
# /timer
# /mode : {"mode": "auto|manual|timer"}


class ReefLedAPI():

    def __init__(self,ip) -> None:
        self._base_url = "http://"+ip
        _LOGGER.debug("API set for %s"%ip)
        self.data={}
        self.last_update_success=None
        
    async def get_initial_data(self):
        _LOGGER.debug('Reefled.get_initial_data')
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.fetch_data)
        #self.fetch_data()
        return self.data

    def fetch_data(self):
        if self.last_update_success:
            up = datetime.datetime.now() - self.last_update_success
            last_update  = up.seconds
        else:
            last_update = 3
        if last_update > 2:
            _LOGGER.debug("fecth_data: %s",self._base_url+"/manual")
            r = requests.get(self._base_url+"/manual",timeout=2)
            if r.status_code == 200:
                response=r.json()
                _LOGGER.debug("Get data: %s"%response)
                try:
                    self.data[WHITE_INTERNAL_NAME]=response['white']/CONVERSION_COEF
                    self.data[BLUE_INTERNAL_NAME]=response['blue']/CONVERSION_COEF
                    self.data[MOON_INTERNAL_NAME]=response['moon']/CONVERSION_COEF
                    self.data[FAN_INTERNAL_NAME]=response['fan']
                    self.data[TEMPERATURE_INTERNAL_NAME]=response['temperature']
                    ##
                    self.last_update_success=datetime.datetime.now()
                    ##
                except Exception as e:
                    _LOGGER.error("Getting values %s"%e)
                    _LOGGER.debug("/*/*/*/* coordinator data updated to %s"%self.data)
        else:
            _LOGGER.debug("No refresh, last data retrieved less than 2s")
    
    async def update(self) :       
        _LOGGER.debug("Reefled.update")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.fetch_data)
        return self.data
    
    
    async def async_request_refresh(self):
        _LOGGER.debug("async_request_refresh")
        await self.update()
        pass
        #await self.update()

    async def async_add_listener(self,callback,context):
        _LOGGER.debug("async_add_listener")
        pass

    def push_values(self):
        _LOGGER.debug("++> set new values: %s"%self.data)
        payload={"white": self.data[WHITE_INTERNAL_NAME]*CONVERSION_COEF, "blue":self.data[BLUE_INTERNAL_NAME]*CONVERSION_COEF,"moon": self.data[MOON_INTERNAL_NAME]*CONVERSION_COEF}
        r = requests.post(self._base_url+'/manual', json = payload)
        _LOGGER.debug(r.text)

    async def async_send_new_values(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None,self.push_values)
        
