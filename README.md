https://www.youtube.com/@MDJUNAINMUNTASIR
This is my youtube channel where all the detailed videos are posted.
Part 1-
Built a circuit that consists of 5 LEDs (any colours) with appropriate resistors, a
button and a LCD as shown in the demo video. Arrange the LEDs in a line and keep the breadboard
as neat as possible. Created a Python program which will light up the LEDs in a travelling pattern as shown in the demo
video. Start the pattern at a pace of your choice. Pressing the button will increase or decrease the
pattern speed in steps (you choose the direction), starting over when maximum or minimum is
reached. The LCD needs to show the pattern speed in percent, which needs to be updated with each button
press.

Part 2-
Added an analog-to-digital converter to the breadboard and a potentiometer. Used parts available in Freenove kit. 
Updateed my program so the potentiometer can be used to continuously adjust brightness of all
LEDs without interrupting the blinking pattern. Added a second line to the LCD, which will indicate
LED brightness in percent.
Consider the following hints:
• Make sure that show_pattern function runs as a thread if not already done.
• Calculate the brightness inside show_pattern functions for loop, based on the
potentiometer input and store it in a variable, called for example brightness. Use a
logarithmic formula or lookup table for best visual results and highest credit.
• Set LED brightness by changing leds[num].on() to leds[num].value = brightness in
show_pattern.
• Create a separate a thread to refresh the LCD 5-10 times a second and add the line to it to
display the brightness.
