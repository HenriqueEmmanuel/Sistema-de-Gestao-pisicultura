#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600); 
  sensors.begin();    
  Serial.println("Sensor DS18B20 iniciado.");
}

void loop() {
  sensors.requestTemperatures();             
  float temperaturaC = sensors.getTempCByIndex(0); 

  Serial.print("Temperatura: ");
  Serial.print(temperaturaC);
  Serial.println(" °C");

  delay(1000); 
}
