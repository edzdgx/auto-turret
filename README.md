# Auto Turret with Raspberry Pi 3
# Project Idea
An embedded system that controls a paintball gun to automatically aim at desired location and pull the trigger. The system is controlled using Raspberry Pi 3, 3 servo motors are used in the design, including one that controls x-axis, one that controls y-axis, and one that controls the trigger. There is also a PiCamera V2 that does color detection and tracking with OpenCV library. Each frame the camera captures is masked and analyzed, and coordinate of the center of the tracked color will be calculated. Then servos will be adjusted through the coordinate information. Servos are controlled by PWM signal that the GPIO pins send out.
* Auto-turret that fires paintballs at desired target (face)
* PiCamera Module V2 to stream images to be processed
* OpenCV library used for facial recognition/ color detection
* 3 servos to control x-axis, y-axis, and trigger of paintball gun
* Raspberry Pi 3 to control and coordinate all parts

# Flow Diagram
![](/flow_diagram.png)

# Components
* 3 * [HS805BB+ servos](https://hitecrcd.com/products/servos/giant-servos/analog-giant-servos/hs-805bb/product)
* 1 * [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* 1 * [PiCamera Module V2](https://www.raspberrypi.org/products/camera-module-v2/)
* 1 * [CO2 tank](https://www.tippmannparts.com/Tippmann-20oz-CO2-Bottle-p/8270.htm)
* 1 * [Paintball Gun](http://www.valken.com/Marker-V-TAC-GT-50-50-caliber)
* 1 * [Breadboard for GPIO](https://www.amazon.com/Qunqi-point-Experiment-Breadboard-5-5%C3%978-2%C3%970-85cm/dp/B0135IQ0ZC/ref=asc_df_B0135IQ0ZC/?tag=hyprod-20&linkCode=df0&hvadid=198091709182&hvpos=1o6&hvnetw=g&hvrand=1395503657577470532&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9010932&hvtargid=pla-407203040794&psc=1)
* 1 * [5V Power Source](https://www.adafruit.com/product/1959)

# PiGPIO Pinout
Pin #  | Component
------------- | -------------
3  | Y-axis Servo
5  | Trigger Servo
6  | Ground
7  | X-axis Servo

# Software Setup
* For facial recognition, use OpenCV  library: 
  * `sudo apt-get install python-opencv`
* For processing frame on PiCamera, use picamera.array library: 
  * `sudo apt-get install python-picamera`
* Used PWM signals to control motion of servos


# Hardware Setups
![](/hardware_setup1.png)

![](/hardware_setup2.png)
Raspberry Pi:
Connect Camera Module V2 to Raspberry Pi with silver band facing the HDMI port. Connect mouse and keyboard using USB port. Connect HDMI with a screen.

Servos:
There are 3 wires connected to each servo (red/black/yellow) each representing power/ground/signal. Red should go directly into an external battery, black should go to ground on breadboard (which is the common ground for all batteries and servos.

# Demo
[Video Demo](https://www.youtube.com/watch?v=N5QmZ92uvUo)
