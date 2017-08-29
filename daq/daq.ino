
void setup() {
  Serial.begin(57600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {
  Serial.print(analogRead(A0));
  Serial.print(' ');
  Serial.print(analogRead(A1));
  Serial.println();
}
