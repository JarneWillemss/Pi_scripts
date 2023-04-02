import time
import orangepi
import math

# Define the pin used to read the LDR value
LDR_PIN = orangepi.GPIO.PA7

# Define the reference voltage for the ADC (in mV)
ADC_REF_VOLTAGE = 3300

# Define the maximum ADC value
ADC_MAX_VALUE = 4095

# Define the resistance of the LDR in darkness (in ohms)
LDR_RESISTANCE_DARK = 10000

# Define the beta value of the LDR (from the datasheet)
LDR_BETA_VALUE = 3975

# Set up the GPIO
orangepi.GPIO.setmode(orangepi.GPIO.BOARD)
orangepi.GPIO.setup(LDR_PIN, orangepi.GPIO.IN)

def read_ldr():
    """Read the analog value from the LDR"""
    value = orangepi.analog.read(LDR_PIN)
    return value

def convert_to_percentage(value):
    """Convert the analog value to a percentage value between 0% and 100%"""
    resistance = (ADC_REF_VOLTAGE / value) * 1000 - LDR_RESISTANCE_DARK
    percentage = math.exp(-math.log(resistance / LDR_RESISTANCE_DARK) / LDR_BETA_VALUE) * 100
    return percentage

# Main loop
try:
    while True:
        # Read the analog value from the LDR
        ldr_value = read_ldr()

        # Convert the analog value to a percentage value
        percentage = convert_to_percentage(ldr_value)

        # Display the percentage value
        print("Light incidence: {:.0f}%".format(percentage))

        # Wait for a short period of time before reading the LDR value again
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# Clean up the GPIO
orangepi.GPIO.cleanup()