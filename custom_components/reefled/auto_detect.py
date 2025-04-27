#!/usr/local/bin/python

import socket
import netifaces
import ipaddress
import requests
from lxml import objectify
from multiprocessing import Pool

def get_local_ips():
    # Get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip=s.getsockname()[0]
    s.close()
    #get subnetwork address and mask
    for netif in netifaces.interfaces():
        try:
            addr=netifaces.ifaddresses(netif)[2][0]
            if addr['addr'] == ip:
                net = ipaddress.ip_network(ip+'/'+addr['netmask'], strict=False)        
                return [str(ip) for ip in ipaddress.IPv4Network(str(net))]
        except:
            pass


def is_reefled(ip):
    device_list=['RSLED160','RSLED90','RSLED50']
    try:
        r = requests.get('http://'+ip+'/description.xml',timeout=2)
        if r.status_code == 200:
            tree = objectify.fromstring(r.text)
            name=tree.device.modelName
            if name in device_list:
               return ip,True
    except:
        pass
    return ip,False

def get_reefleds(nb_of_threads=64):
    ips=get_local_ips()
    reefleds=[]
    with Pool(nb_of_threads) as p:
        res=p.map(is_reefled,ips)
        for device in res:
            ip,status=device
            if status == True:
                reefleds+=[ip+' '+get_friendly_name(ip)]
    return reefleds
                

def get_unique_id(ip):
    try:
        r = requests.get('http://'+ip+'/description.xml',timeout=2)
        if r.status_code == 200:
            tree = objectify.fromstring(r.text)
            udn=str(tree.device.UDN)
            uuid=udn.replace("uuid:","")
            return uuid
    except Exception as e :
        return str(e)
     
def get_friendly_name(ip):
    try:
        r = requests.get('http://'+ip+'/description.xml',timeout=2)
        if r.status_code == 200:
            tree = objectify.fromstring(r.text)
            name=str(tree.device.friendlyName)
            return name
    except:
        pass
    return None


if __name__ == '__main__':
    print(get_unique_id("192.168.0.194"))
    print(get_friendly_name("192.168.0.194"))
    
          #nb_of_threads=255
#    res=get_reefleds(nb_of_threads)
#    print(res)
