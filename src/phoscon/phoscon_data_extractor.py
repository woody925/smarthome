import json
import os
import sys

current_dir = os.path.dirname( __file__ )
mongodb_include_dir = os.path.join( current_dir, '..', 'database')
sys.path.append( mongodb_include_dir )
import mongodb_handler

from phoscon_handler import Phoscon_Handler

def read_temp_data(json_data, name_of_sensor):
    for x in json_data:
        if json_data[x].get('name') == name_of_sensor and json_data[x].get('config').get('reachable') == True:
            print(name_of_sensor, " found and sensor is reachable")
            if 'temperature' in json_data[x].get('state'):
                print("Temperature: " + str((json_data[x].get('state').get('temperature')/100)) + " °C")
            if 'humidity' in json_data[x].get('state'):
                print("Humidity: " + str(json_data[x].get('state').get('humidity')/100) + " %")
            if 'pressure' in json_data[x].get('state'):
                print("Pressure: " + str(json_data[x].get('state').get('pressure')) + " hPa")
    return

def return_sensor_data(json_data, name_of_sensor):
    '''returns array of [temp, humidity, pressure] '''
    current_sensor_values = []
    for x in json_data:
        if json_data[x].get('name') == name_of_sensor and json_data[x].get('config').get('reachable') == True:
            if 'temperature' in json_data[x].get('state'):
                current_sensor_values.append((json_data[x].get('state').get('temperature')/100))
            if 'humidity' in json_data[x].get('state'):
                current_sensor_values.append(json_data[x].get('state').get('humidity')/100)
            if 'pressure' in json_data[x].get('state'):
                current_sensor_values.append(json_data[x].get('state').get('pressure'))
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(current_sensor_values)
    print("++++++++++++++++++++++++++++++++++++++++++")
    return current_sensor_values


def fetching_data_from_sensors():
    phoscon_handle = Phoscon_Handler()
    phoscon_response = phoscon_handle.get_sensor_data_all()
    json_data = phoscon_response.json()

    # return_sensor_data(json_data, 'Temp-Wohnzimmer')
    # return_sensor_data(json_data, 'Temp-Badezimmer')
    transfer_sensor_data_to_db(json_data, 'Temp-Wohnzimmer')
    transfer_sensor_data_to_db(json_data, 'Temp-Badezimmer')

def transfer_sensor_data_to_db(json_data, name_of_sensor):
    '''transfer sensor data to db if sensor is reachable'''
    current_sensor_values = []
    print("########################")
    print(json_data)
    print("########################")
    for x in json_data:
        if json_data[x].get('name') == name_of_sensor and json_data[x].get('config').get('reachable') == True:
            mongodb_handler.MongoDBHandler.insert_one(json_data[x], "smarthome", "sensors_log")
            if 'etag' in json_data[x]:
                current_sensor_values.append(json_data[x].get('etag'))
            if 'temperature' in json_data[x].get('state'):
                current_sensor_values.append((json_data[x].get('state').get('temperature')/100))
            if 'humidity' in json_data[x].get('state'):
                current_sensor_values.append(json_data[x].get('state').get('humidity')/100)
            if 'pressure' in json_data[x].get('state'):
                current_sensor_values.append(json_data[x].get('state').get('pressure'))
    print(current_sensor_values)
    return current_sensor_values


print("Starting program...")
mongodb_handler.MongoDBHandler.init_mongodb()

fetching_data_from_sensors()
print("Ending program...")



