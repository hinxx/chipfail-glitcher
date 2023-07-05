// dummy target for inspecting power / glitch signals and
// supplying trigger to glitcher FPGA
// tested on RP2040

// make sure python script for glitching notices the trigger


int led = LED_BUILTIN;

int trig_out = D12;   // trigger : target -> glitcher
int power_in = D11;   // power   : glitcher -> target
int glitch_in = D13;  // glitch  : glitcher -> target

int power_state = -1;
bool power_print = true;

int glitch_state = -1;
bool glitch_print = true;

int trigger_state = -1;
bool trigger_print = true;

unsigned long t0Micros = 0;
unsigned long t1Micros = 0;
const long interval = 1500;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(trig_out, OUTPUT);
  pinMode(power_in, INPUT);
  pinMode(glitch_in, INPUT);

  digitalWriteFast(trig_out, LOW);
  trigger_state = 0;

  Serial.begin(115200);
  while (!Serial) ; // Serial is via USB; wait for enumeration
  Serial.println("Target ready!");
  Serial.println("TRIGGER OFF");
}

void loop() {
  // digitalWrite(led, LOW);
  // delay(300);
  // digitalWrite(led, HIGH);
  // delay(300);

  if (digitalReadFast(power_in)) {
    if (! power_state) {
      power_print = true;
    }
    power_state = 1;
    if (power_print) {
      Serial.println("POWER ON");
      power_print = false;
      digitalWriteFast(led, HIGH);

      // enter the state to generate the trigger      
      trigger_state = 1;
      t0Micros = micros();
    }
  } else {
    if (power_state) {
      power_print = true;
    }
    power_state = 0;
    if (power_print) {
      Serial.println("POWER OFF");
      power_print = false;
      digitalWriteFast(led, LOW);
    }
  }

  if (digitalReadFast(glitch_in)) {
    if (! glitch_state) {
      glitch_print = true;
    }
    glitch_state = 1;
    if (glitch_print) {
      Serial.println("GLITCH ON");
      glitch_print = false;
      digitalWriteFast(led, HIGH);
    }
  } else {
    if (glitch_state) {
      glitch_print = true;
    }
    glitch_state = 0;
    if (glitch_print) {
      Serial.println("GLITCH OFF");
      glitch_print = false;
      digitalWriteFast(led, LOW);
    }
  }

  if (trigger_state == 1) {
    t1Micros = micros();
    if (t1Micros - t0Micros >= interval) {
      Serial.println("TRIGGER ON");
      // set trigger output high
      digitalWriteFast(trig_out, HIGH);
      trigger_state = 2;
      t0Micros = micros();
    }
  } else if (trigger_state == 2) {
    t1Micros = micros();
    if (t1Micros - t0Micros >= interval) {
      // set trigger output low
      digitalWriteFast(trig_out, LOW);
      trigger_state = 0;
      Serial.println("TRIGGER OFF");
    }
  }

}
