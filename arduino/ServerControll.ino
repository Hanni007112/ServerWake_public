#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192,168,2, 113);
IPAddress gateway(192,168,2, 1);
IPAddress subnet(255, 255, 0, 0);
EthernetServer server(23);
IPAddress allowedIP(192, 168, 2, 110);

int relayPin = 3;
int checkPowerPin= 2;

String powerOnPassword = "Test";
String powerOffPassword = "1234";
char buffer[80];
int index = 0;

void setup() {

  Ethernet.begin(mac, ip, gateway, subnet);
  server.begin();

  Serial.begin(9600);
   while (!Serial) {
  }

  Serial.print("Chat server address:");
  Serial.println(Ethernet.localIP());

  pinMode(relayPin, OUTPUT);
  pinMode(checkPowerPin, INPUT);
  digitalWrite(checkPowerPin, HIGH);
}

void triggerRelay(){
  digitalWrite(relayPin, HIGH);
  delay(100);
  digitalWrite(relayPin, LOW);
  }

bool checkPower(){
  return digitalRead(checkPowerPin) == LOW;
  }

void loop() {
  EthernetClient client = server.available();
  /*while (true){Serial.println(checkPower());}*/

  if (client) {
    if (false){/*allowedIP != client.remoteIP()){*/
      client.stop();
      }
    if (client.available() > 0) {

      char c = client.read();
      if(index < sizeof buffer - 1)
      {
         buffer[index] = c;
         index++;
         buffer[index] = '\0';
      }
      
      if(client.available() == 0){
        Serial.print(client.remoteIP()); 
        Serial.print(": ");
        Serial.println(buffer);         
        
        if (powerOnPassword.compareTo(String(buffer)) == 0){/*allowedIP == client.remoteIP()){*/
          if ( checkPower()){client.write("alreadyOn");Serial.println("alreadyOn");}
          else {
            client.write("success");
            Serial.println("success");
            triggerRelay();
          }

        }
        else if (powerOffPassword.compareTo(String(buffer)) == 0){
          if ( !checkPower()){client.write("alreadyOff");Serial.println("alreadyOff");}
          else {
            client.write("success");
            Serial.println("success");
            triggerRelay();
          } 
         }
         else{
          client.write("failure");
          Serial.println("failure");
          }
          
         Serial.println("disconnecting.");
         memset(buffer, 0, sizeof buffer);
         index = 0;
         client.flush();
         client.stop();
      }
    }
  }
}