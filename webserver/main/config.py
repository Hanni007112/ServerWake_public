import json
import os
from django.core.management.utils import get_random_secret_key


def createConfig(path):
    print("creating config")
    dictionary = {
        "powerOnPassword" : "Test",
        "powerOffPassword" : "1234",
        "arduinoPort" : "23",
        "arduinoIp" : "###",
        "serverIp" : "###",
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
configFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
if not os.path.isfile(configFilePath):
    createConfig(configFilePath)

with open(configFilePath) as json_file:
    config = json.load(json_file)