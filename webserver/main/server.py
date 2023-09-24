import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import paramiko
import os
import telnetlib

import datetime

from .config import config
from .models import ServerAllocation, ServerPing

tz=datetime.timezone.utc

def now():
    return datetime.datetime.now(tz=tz)

def get_serverAllocation(time : datetime.datetime):
    return ServerAllocation.objects.filter(endTime__gt = time, startTime__lte = time,  active=True)

def nextShutdown():
    if  not get_serverAllocation(now()).exists():
        return False
    
    checkTime = now()
    i= 0
    while get_serverAllocation(checkTime).exists() and i < 100:
        i += 1
        checkTime = get_serverAllocation(checkTime).first().endTime
    if i >= 100:
        return False
    return checkTime

def ping(host):
    createNew = False
    if host == config["serverIp"]: 
        createNew = True
        try:
            latest = ServerPing.objects.latest()
            createNew = (now() - latest.timestamp) > datetime.timedelta(minutes=10)
        except ServerPing.DoesNotExist: 
            pass

    time = 0.2
    if platform.system().lower()=='windows':
        command = ['ping', "-n", '1',  '-w' , str(time * 1000), host]
    else:
        command = ['ping', "-c", '1',  '-W' , str(time), host]
    FNULL = open(os.devnull, 'w')
    successful = subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT) == 0
    if createNew : ServerPing.objects.create(timestamp = now(), successful = successful)
    return successful

class alreadyOff(Exception):
    pass
class alreadyOn(Exception):
    pass
class alreadyStarting(Exception):
    pass

def controllServer(state: bool):
    if not config["controllServer"] :
        return True
    if not ping(config['arduinoIp']):
        print("Cant reach Arduino")
        return False
    
    if state == ping(config['serverIp']):
        #something is not right
        if state: raise alreadyOn
        else: raise alreadyOff

    if state:   # powerOn
        message = (config['powerOnPassword']).encode('ascii')
    else:       # powerOff
        message = (config['powerOffPassword']).encode('ascii')
    
    try:
        telnetObj=telnetlib.Telnet(config['arduinoIp'], config['arduinoPort'])
        telnetObj.write(message)
        output=telnetObj.expect([b"success", b"failure", b"alreadyOff", b"alreadyOn"],timeout=0.1)
        telnetObj.close()
    except Exception as ex:
        print(ex)
        telnetObj.close()
        return False
    outputString = output[2]

    if outputString == b"alreadyOff" : raise alreadyOff
    if outputString == b"alreadyOn": raise alreadyStarting
    if outputString == b"failure": return False
    return  outputString == b"success"
