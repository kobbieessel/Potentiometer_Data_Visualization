#define led 6
#define pot A0

uint8_t brightness;
uint16_t pot_value;

void setup(void){
 Serial.begin(115200);
 pinMode(led, OUTPUT);
 pinMode(pot, INPUT);
}

void loop(void){
  pot_value = analogRead(pot);
  brightness = (255.0/1023.0) * pot_value;
  analogWrite(led, brightness);
  Serial.println(pot_value);
  delay(500);
}