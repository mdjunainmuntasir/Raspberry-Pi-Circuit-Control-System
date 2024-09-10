#!/usr/bin/python3
# Program: LNX255 Project 03 
# Student: Md. Junain Muntasir
# Date: July 2024

from gpiozero import PWMLED, Button
from signal import pause, signal, SIGTERM, SIGHUP
from time import sleep
from threading import Thread
from rpi_lcd import LCD

# Initialize delay variables
min_delay = 0.1
max_delay = 0.5
delay_step = 0.1
delay = min_delay
speed_percent = int((min_delay / delay_step) * 100)
active = True

# Using specified GPIO pins for LEDs
leds = (
    PWMLED(27), 
    PWMLED(22), 
    PWMLED(13), 
    PWMLED(19), 
    PWMLED(26)
)

# Using specified GPIO pin for the button
button = Button(16)

# Initialize the LCD
lcd = LCD()

# Cleanup function to handle termination signals
def cleanup(signum, frame):
    exit(1)

# Function to change speed when the button is pressed
def change_speed():
    global delay, speed_percent

    delay += delay_step
    if delay > max_delay:
        delay = min_delay

    speed_percent = int((1 - (delay - min_delay) / (max_delay - min_delay)) * 100)
    lcd.text(f"Speed: {speed_percent}%", 1)

# Function to display the LED pattern
def show_pattern():
    try:
        while active:
            for num in (0, 1, 2, 3, 4, 3, 2, 1):
                leds[num].on()
                sleep(delay)
                leds[num].off()
    except AttributeError:
        pass

try:
    # Set up signal handlers for clean termination
    signal(SIGTERM, cleanup)
    signal(SIGHUP, cleanup)

    # Configure button press to change speed
    button.when_pressed = change_speed

    # Start LED pattern thread
    pattern_thread = Thread(target=show_pattern)
    pattern_thread.start()

    # Display initial speed on the LCD
    lcd.text(f"Speed: {speed_percent}%", 1)

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
