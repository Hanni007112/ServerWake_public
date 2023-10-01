import json
import os
from django.core.management.utils import get_random_secret_key


def createConfig(path):
    print("creating config")
    dictionary = {
        "powerOnPassword" : "Test",
        "powerOffPassword" : "1234",
        "arduinoPort" : "23",
        "arduinoIp" : "192.168.1.2",
        "serverIp" : "192.168.1.2",
        "adminMaxAllocation" : 48,
        "normalMaxAllocation" : 4,
        "allowedHosts" : ["*"],
        "trustedOrigins" : [],
        "debug" : True,
        "TZ" : "Europe/Berlin",
        "Interval" : 30,
        "secretKey" : get_random_secret_key(),
        "controllServer": True
        }
    json_object = json.dumps(dictionary, indent=4)
    with open(path, 'x') as json_file:
        json_file.write(json_object)

# Opening JSON file
dataFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '/DATA'))
configFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '/DATA/config.json'))
if not os.path.isdir(dataFilePath):
    os.mkdir(dataFilePath)
if not os.path.isfile(configFilePath):
    createConfig(configFilePath)

with open(configFilePath) as json_file:
    config = json.load(json_file)