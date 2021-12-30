import requests
import time
import json

import mongodb_handler

############################################################################
# Function which takes the response json file and extract temp sensor data #
############################################################################
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


def fetching_sensor_data(sensors_url):
    '''Fetch sensor data of sensors url and returns it'''
    return requests.get(sensors_url)




url = "http://192.168.178.44:80/api"
data_api_request = {'devicetype': 'fetchingDataFromSensors'}

#print("Fetching info regarding local API server...")

#response = requests.get("https://dresden-light.appspot.com/discover")
#print(response.status_code)
#print(response.json())


# Aquire an API key
#response_apiRequest = requests.post(url, json = data_api_request)
#print(response_apiRequest.text)
# username: 47C22DE829

response = fetching_sensor_data("http://192.168.178.5:8080/api/47C22DE829/sensors")
json_data = response.json()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

#print(response.headers['content-type'])
#print(response.json())
#print("Parsed list of users: " + str(type(json_data)))
#print(len(json_data))
#print("")
#print("Print the dict:")
#print(json_data)
#print("############################################")
#for x in json_data:
 #   print(json_data[x].get('name'))

#print("First element of list: " + str(type(json_data['1'])))
print("############################################")

read_temp_data(response.json(), 'Temp-Wohnzimmer')
read_temp_data(response.json(), 'Temp-Badezimmer')



# End of this program
print("Stop program!")

