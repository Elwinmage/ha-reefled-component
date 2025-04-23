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
    STATUS_INTERNAL_NAME,
    IP_INTERNAL_NAME,
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
# /auto
# /auto/[1-7]
# /preset_name
# /preset_name/[1-7]
# /cloud
# /clouds/[1-7] (intensity: Low,Medium,High)

class ReefLedAPI():

    def __init__(self,ip) -> None:
        self._base_url = "http://"+ip
        _LOGGER.debug("API set for %s"%ip)
        self.data={}
        self.data[STATUS_INTERNAL_NAME]=False
        self.programs={}
        self.last_update_success=None
        
    async def get_initial_data(self):
        _LOGGER.debug('Reefled.get_initial_data')
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.fetch_data)
        return self.data
    

    def fetch_data(self):
        if self.last_update_success:
            up = datetime.datetime.now() - self.last_update_success
            last_update  = up.seconds
        else:
            last_update = 3
        if last_update > 2:
            self._fetch_led_status()
            self._fetch_program()
        else:
            _LOGGER.debug("No refresh, last data retrieved less than 2s")

            
    def _fetch_program(self):
        #get week
        _LOGGER.debug("_fetch_progam")
        r= requests.get(self._base_url+"/preset_name",timeout=2)
        if r.status_code==200:
            response=r.json()
            _LOGGER.debug("Get data:%s"%response)
            try:
                for i in range(1,8):
                    _LOGGER.debug(" * %d %s"%(response[i-1]['day'],response[i-1]['name']))
                    prog_id=response[i-1]['day']
                    prog_name=response[i-1]['name']
                    clouds_data={}
                    if prog_name not in self.programs:
                        r = requests.get(self._base_url+"/auto/"+str(prog_id),timeout=2)
                        if r.status_code==200:
                            prog_data=r.json()
                            self.programs[prog_name]=prog_data
                            _LOGGER.debug("Get prog: %s"%prog_data)
                    else:
                        prog_data=self.programs[prog_name]

                    # Get clouds
                    c = requests.get(self._base_url+"/clouds/"+str(prog_id),timeout=2)
                    if c.status_code==200:
                        clouds_data=c.json()
                        _LOGGER.debug("Get clouds: %s"%clouds_data)
                        
                    self.data['auto_'+str(prog_id)]={'name':prog_name,'data':prog_data,'clouds':clouds_data}
            except Exception as e:
                _LOGGER.error("Can not get value: %s"%response)
                _LOGGER.error("Can not get value: %s"%e)
                

                
    def _fetch_led_status(self):
        _LOGGER.debug("fecth_data: %s",self._base_url+"/manual")
        r = requests.get(self._base_url+"/manual",timeout=2)
        if r.status_code == 200:
            response=r.json()
            _LOGGER.debug("Get data: %s"%response)
            try:
                self.data[WHITE_INTERNAL_NAME]=int(response['white']/CONVERSION_COEF)
                self.data[BLUE_INTERNAL_NAME]=int(response['blue']/CONVERSION_COEF)
                self.data[MOON_INTERNAL_NAME]=int(response['moon']/CONVERSION_COEF)
                self.data[FAN_INTERNAL_NAME]=response['fan']
                self.data[TEMPERATURE_INTERNAL_NAME]=response['temperature']
                if ( self.data[WHITE_INTERNAL_NAME]>0 or
                     self.data[BLUE_INTERNAL_NAME]>0 or
                     self.data[MOON_INTERNAL_NAME]>0 ):
                    self.data[STATUS_INTERNAL_NAME]= True
                else:
                    self.data[STATUS_INTERNAL_NAME]= False
                
                ##
                self.last_update_success=datetime.datetime.now()
                ##
            except Exception as e:
                _LOGGER.error("Getting values %s"%e)
                _LOGGER.debug("/*/*/*/* coordinator data updated to %s"%self.data)
    
    
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


    def get_initial_values(self):
        r = requests.get(self._base_url+'/',timeout=2)
        if r.status_code == 200:
            response=r.json()
            _LOGGER.debug("**** /* /* */ */ **** %s" %response)
            self.data[IP_INTERNAL_NAME]=response['wifi_ip']

        
    async def async_first_refresh(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None,self.get_initial_values)
        
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
        
