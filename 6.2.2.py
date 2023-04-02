import time
import wiringpi

def ActivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 0) # Activate ADC using CS
    time.sleep(0.000005)

def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1) # Deactivate ADC using CS
    time.sleep(0.000005)

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1, (8+adcnum)<<4, 0]))
    time.sleep(0.000005)
    adcout = ((recvData[1]&3) << 8) + recvData[2]
    return adcout

# Setup
pin_CS_adc = 16 # We will use w16 as CE, not the default pin w15!
pin_led_a = 18 # Set pin 18 for LED A
pin_led_b = 19 # Set pin 19 for LED B
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin_CS_adc, 1) # Set CE to mode 1 (OUTPUT)
wiringpi.pinMode(pin_led_a, 1) # Set LED A pin to mode 1 (OUTPUT)
wiringpi.pinMode(pin_led_b, 1) # Set LED B pin to mode 1 (OUTPUT)
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0) # (channel, port, speed, mode)

# Main
try:
    threshold_high = 650
    threshold_low = 550
    hysteresis_gap = 25
    led_a_on = False
    led_b_on = False
    
    while True:
        ActivateADC()
        voltage = readadc(0) # Read voltage from channel 0
        DeactivateADC()
        print("Voltage:", voltage)
        
        # Control LEDs based on voltage
        if voltage < threshold_low - hysteresis_gap and not led_a_on:
            wiringpi.digitalWrite(pin_led_a, 1) # Turn on LED A
            wiringpi.digitalWrite(pin_led_b, 0) # Turn off LED B
            led_a_on = True
            led_b_on = False
        elif voltage > threshold_high + hysteresis_gap and not led_b_on:
            wiringpi.digitalWrite(pin_led_a, 0) # Turn off LED A
            wiringpi.digitalWrite(pin_led_b, 1) # Turn on LED B
            led_a_on = False
            led_b_on = True
            
        time.sleep(0.2)

except KeyboardInterrupt:
    wiringpi.digitalWrite(pin_led_a, 0) # Turn off LED A
    wiringpi.digitalWrite(pin_led_b, 0) # Turn off LED B
    DeactivateADC()
    print("\nProgram terminated")