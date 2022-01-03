from phoscon_handler import Phoscon_Handler
import json

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

    return_sensor_data(json_data, 'Temp-Wohnzimmer')
    return_sensor_data(json_data, 'Temp-Badezimmer')



print("Starting program...")
fetching_data_from_sensors()
print("Ending program...")



