# ServerWake
a Project to power on and off a Server remotely.

There are many improvements to make, feel free to commit to this project!

## Prerequisites
* a Server (the one you want to controll)
* a Arduino (to close the Power Pins)
* a Server (on which the webserver is running)

## Arduino
### Circuit
U need:
* Ethernet Shield
* 1 Relays
* 1 Transistor
* Resistors
* Jumper Wires

After installing the ethernet shield follow this diagram to connect the remaining components.

![circuit diagram](/arduino/ServerControll.svg?raw=true)

### Code
the Code is found [here](/arduino/ServerControll.ino).

U have to change the following things:
* Ip (local Ip of the Server)
* gateway
* subnet
* server (Port)
* powerOnPassword
* powerOffPassword
* allowed Ip
* maybe the mac-address 
 
 ## Webserver
 
 This project is using a django based webserver. 
 
 before Using the Server u need to:
 * create a superuser to giver permission to other users and yourself 
 ``` cmd
 python manage.py createsuperuser 
 ```
 * edit the config.json, created at first startup of the webserver
