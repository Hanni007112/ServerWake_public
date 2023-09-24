import sys
import telnetlib


HOST = "192.168.2.113"
PORT = "23"

PowerOnPassword = "Test"
PowerOffPassword = "1234"

telnetObj=telnetlib.Telnet(HOST,PORT)
message = (PowerOffPassword).encode('ascii')
telnetObj.write(message)
output=telnetObj.expect([b"success", b"failure", b"alreadyOff", b"alreadyOn"],timeout=0.1)
outputString = output[2]
if outputString == "success" :
    print("\(^_^)/")
else:
    print(r"/(°_°)\\")
print(outputString)
telnetObj.close()

