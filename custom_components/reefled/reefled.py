import logging
import threading
import json
import time

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import requests

from .const import (
    DOMAIN,
    CONFIG_FLOW_IP_ADDRESS,
    DEFAULT_PULL_RATE,
    FAN_INTERNAL_NAME,
    TEMPERATURE_INTERNAL_NAME,
    WHITE_INTERNAL_NAME,
    BLUE_INTERNAL_NAME,
    MOON_INTERNAL_NAME
)

_LOGGER = logging.getLogger(__name__)

class ReefLed(threading.Thread):

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._entry = entry
        ip=entry.data[CONFIG_FLOW_IP_ADDRESS]
        self._base_url = "http://"+ip
        self._name = entry.title
        #Entities
        self._data = {}
        self._data['white']=0
        self._data['blue']=0
        self._data['moon']=0
        self._data[FAN_INTERNAL_NAME]=0
        self._data[TEMPERATURE_INTERNAL_NAME]=0
        threading.Thread.__init__(self, name=self._name)
        
    def is_alive(self):
        return self._alive
        
    def start_polling(self):
        _LOGGER.debug("Start polling for %s at %s"%(self._name,self._base_url))
        self._alive = True
        self.start()

    def stop_polling(self):
        _LOGGER.debug("Stop polling for %s at %s"%(self._name,self._base_url))        
        self._alive = False
        self.join(2)

    def get_value(self,name):
        _LOGGER.debug("get new value %s"%name)
        return self._data[name]
        
    def set_value(self,name,value):
        _LOGGER.debug("set new value %s"%name)
        self._data[name]=value
        #TODO implementer la commande REST
        
    def run(self):
        time.sleep(5)
        while self._alive:
            sleep_time=DEFAULT_PULL_RATE
            r = requests.get(self._base_url+"/manual",timeout=2)
            if r.status_code == 200:
                response=r.json()
                _LOGGER.debug("Get data: %s"%response)
                try:
                    self._data[WHITE_INTERNAL_NAME]=response['white']
                    self._data[BLUE_INTERNAL_NAME]=response['blue']
                    self._data[MOON_INTERNAL_NAME]=response['moon']
                    self._data[FAN_INTERNAL_NAME]=response['fan']
                    self._data[TEMPERATURE_INTERNAL_NAME]=response['temperature']
                except Exception as e:
                    _LOGGER.error("Getting values %s"%e)
                    sleep_time=5
            time.sleep(sleep_time)

            
