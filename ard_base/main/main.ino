#include "SoftwareSerial.h"
#include "ArduinoJson.h"

#define TEMP_ANALOG_IN A5
#define ANALOG_IN_PIN A4
#define SIREN A10
#define RELAY 35
#define F1 A2
#define F2 A3

String fpsf, pcnt, noww;

const size_t CAPACITY = JSON_OBJECT_SIZE(1);
char in[2048];

SoftwareSerial nexti(19, 18);

float adc_voltage = 0.0;
float in_voltage = 0.0;

float R1 = 30000.0;
float R2 = 7500.0;

float ref_voltage = 5.0;

int temp_analog_out;
int temp_revised_out;
int celcius;

int la, lo, f1, f2;
int adc_value;
int bat;
int i;

bool st, on, br;
double dis;

void warningSiren() {
  analogWrite(SIREN, 255);
  delay(500);
  analogWrite(SIREN, 0);
  delay(500);
}

void updateFlexes() {
  f1 = analogRead(F1);
  f2 = analogRead(F2);
}

void syscall() {
  nexti.write(0xff);
  nexti.write(0xff);
  nexti.write(0xff);
}

void timeShow() {
  nexti.print("tempot.txt=\"" + noww + String("\""));
  syscall();
}

void battery() {
  nexti.print("bat.txt=\"" + String(bat) + String("\""));
  syscall();
}

void fpsd() {
  nexti.print("fps.txt=\"" + fpsf + String("\""));
  syscall();
}

void distance() {
  nexti.print("dis.txt=\"" + String(dis) + String("\""));
  syscall();
}

void lights() {
  nexti.print("switch.bco=");

  if (on) {
    nexti.print("5704");
  } else {
    nexti.print("63488");
  }

  syscall();

  nexti.print("stxt.txt=\"");

  if (on) {
    nexti.print("ON\"");
  } else {
    nexti.print("OFF\"");
  }

  syscall();

  nexti.print("stxt.bco=");

  if (on) {
    nexti.print("5704");
  } else {
    nexti.print("63488");
  }

  syscall();

  nexti.print("sic.pic=");

  if (on) {
    nexti.print("4");
  } else {
    nexti.print("5");
  }

  syscall();
}

void count() {
  nexti.print("pcnt.txt=" + String("\"") + pcnt + String("\""));
  syscall();
}

void updateTemp() {
  nexti.print("tempo.txt=\"" + String(celcius) + String("\""));
}

void update_vals() {
  if (Serial.available()) {
    memset(in, '\0', 2048);

    StaticJsonDocument<CAPACITY> doc;

    for (i = 0; Serial.available(); i ++) {
      in[i] = Serial.read();
      delay(10);
    }

    DeserializationError error = deserializeJson(doc, in);

    if (!error) {
      if (st) {
        const char * pers = doc["perc"];
        const char * fpss = doc["fpsf"];
        const char * brea = doc["brea"];
        const char * nows = doc["noww"];

        noww = nows;

        if (String(brea) == "t") {
          br = true;
        } else {
          br = false;
        }

        pcnt = pers;
        fpsf = fpss;
        Serial.println("NERGIZ");
      } else {
        st = true;
        Serial.println("UMIT");
      }
      Serial.println("Hello");
    } else {
      Serial.println("FUCK");
    }
  } else {
    Serial.println("NOR");
  }
}

void send_vals() {
  StaticJsonDocument<CAPACITY> doc;
  doc["lati"] = String(la), doc["long"] = String(lo);
  doc["f1"] = String(f1), doc["f2"] = String(f2);

  serializeJson(doc, Serial);
}

int thermistor(int temp_raw) {
  double temp;
  temp = log(10240000 / temp_raw - 10000);
  temp = 1 / (0.001129148 + ( 0.000234125 * temp ) + (0.0000000876741 * temp * temp * temp));
  temp = temp - 273.15;
  return temp;
}

void setup() {
  pinMode(TEMP_ANALOG_IN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(SIREN, OUTPUT);
  pinMode(RELAY, OUTPUT);

  digitalWrite(RELAY, HIGH);
  
  Serial.begin(9600);
  nexti.begin(9600);

  la = 2300, lo = 2700, f1 = 0, f2 = 0, dis = 0;
  st = true, on = true, br = false;
}

void loop() {
  temp_analog_out = analogRead(TEMP_ANALOG_IN);
  temp_revised_out = map(temp_analog_out, 0, 1023, 1023, 0);

  celcius = thermistor(temp_revised_out);

  updateTemp();

  adc_value = analogRead(ANALOG_IN_PIN);

  adc_voltage  = (adc_value * ref_voltage) / 1024.0;
  in_voltage = adc_voltage*(R1+R2)/R2;

  bat = in_voltage * 100 / 8.4;

  updateFlexes();
  update_vals();
  timeShow();
  send_vals();
  battery();
  count();
  fpsd();
  lights();
  distance();

  if (br) {
    warningSiren();
  } else {
    delay(1000);
  }
}