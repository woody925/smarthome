#######################################################################################
# File: phoscon_handler.py
# Function: Provides Phoscon class for direct access to the Phoscon Service
#           Provides Phoscon handler class for user to interact with Phoscon
#
#
#######################################################################################


import requests


class Phoscon(object):

    @staticmethod
    def phoscon_get(url):
        '''Fetch phoscon data of api end point and returns it'''
        return requests.get(url)

class Phoscon_Handler(object):
    def __init__(self):
        pass
    
    def get_sensor_data_all(self):
        return Phoscon.phoscon_get("http://192.168.178.5:8080/api/47C22DE829/sensors")

    def set_switch(self, url, value):
        pass

    def set_light(self, url, value):
        pass