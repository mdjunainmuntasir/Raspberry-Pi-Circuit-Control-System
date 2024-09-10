#!/usr/bin/python3
# Program: LNX255 Project 03
# Student: Md. Junain Muntasir
# Date: July 2024

from gpiozero import PWMLED, Button
from signal import pause, signal, SIGTERM, SIGHUP
from time import sleep
from threading import Thread
from smbus import SMBus
from rpi_lcd import LCD
from math import log10, pow
import sys

# Initialize the ADC
bus = SMBus(1)
ADC_ADDRESS = 0x4b  # Updated with the correct I2C address
steps = 255  # Define the steps for the ADC
fade_factor = steps * log10(2) / log10(steps)
active = True
min_delay = 0.1
max_delay = 0.5
delay_step = 0.1
delay = min_delay

# Using specified GPIO pins for LEDs
leds = (
    PWMLED(4),
    PWMLED(17),
    PWMLED(12),
    PWMLED(16),
    PWMLED(20)
)

# Using specified GPIO pin for the switch
speed_switch = Button(25)

# Initialize the LCD
lcd = LCD()

def safe_exit(signum, frame):
    global active
    active = False
    lcd.clear()
    exit(1)

def read_adc(channel):
    try:
        bus.write_byte(ADC_ADDRESS, 0x40 | channel)
        value = bus.read_byte(ADC_ADDRESS)
        print(f"ADC Value: {value}")  # Debug: Print the ADC value
        return value
    except Exception as e:
        print(f"Error reading ADC: {e}", file=sys.stderr)
        return 0

def calculate_brightness():
    while True:
        value = read_adc(0)  # Read from ADC channel A0
        brightness = (pow(2, (value / fade_factor)) - 1) / steps
        yield brightness, int(brightness * 100)  # Return both brightness and brightness_percent

def change_speed():
    global delay
    delay += delay_step
    if delay > max_delay:
        delay = min_delay

    speed_percent = int((1 - (delay - min_delay) / (max_delay - min_delay)) * 100)
    lcd.text(f"Speed: {speed_percent}%", 1)

def show_pattern():
    brightness_gen = calculate_brightness()
    try:
        while active:
            brightness, brightness_percent = next(brightness_gen)
            lcd.text(f"Brightness: {brightness_percent}%", 2)

            # Display speed on the first line
            speed_percent = int((1 - (delay - min_delay) / (max_delay - min_delay)) * 100)
            lcd.text(f"Speed: {speed_percent}%", 1)

            for num in range(5):
                leds[num].value = brightness
                sleep(delay)
                leds[num].off()
    except AttributeError as e:
        print(f"AttributeError: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

try:
    # Set up signal handlers for clean termination
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    # Display initial speed on the LCD
    speed_percent = int((1 - (delay - min_delay) / (max_delay - min_delay)) * 100)
    lcd.text(f"Speed: {speed_percent}%", 1)

    # Configure button press to change speed
    speed_switch.when_pressed = change_speed

    # Start LED pattern thread
    pattern_thread = Thread(target=show_pattern)
    pattern_thread.start()

    # Wait indefinitely until interrupted
    pause()

except KeyboardInterrupt:
    pass

finally:
    # Clean up resources on exit
    active = False
    pattern_thread.join()
    lcd.clear()
    for led in leds:
        led.close()
    sleep(0.25)
