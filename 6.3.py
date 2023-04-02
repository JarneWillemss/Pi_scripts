import wiringpi
import time

# Setup
LM35_pin = 0 # Analog pin connected to LM35
wiringpi.wiringPiSetup()
wiringpi.wiringPiSPISetupMode(0, 1000000, 0) # (channel, speed, mode)

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(0, bytes([1, (8+adcnum)<<4, 0]))
    time.sleep(0.00005)
    adcout = ((recvData[1]&3) << 8) + recvData[2]
    return adcout

try:
    while True:
        voltage = readadc(LM35_pin) # Read voltage from LM35
        temperature = voltage * 0.1 # Convert voltage to temperature (10 mV per degree)
        print("Temperature:", temperature, "C")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated")