# auto-turret
# project idea
An embedded system that controls a paintball gun to automatically aim at desired location and pull the trigger. The system is controlled using Raspberry Pi 3, 3 servo motors are used in the design, including one that controls x-axis, one that controls y-axis, and one that controls the trigger. There is also a PiCamera V2 that does color detection and tracking with OpenCV library. Each frame the camera captures is masked and analyzed, and coordinate of the center of the tracked color will be calculated. Then servos will be adjusted through the coordinate information. Servos are controlled by PWM signal that the GPIO pins send out.

# instructions

# code
All code is included in the repository.

# hardware setups 
![](/images/hardware_setup1.jpg)
Raspberry Pi:
Connect Camera Module V2 to Raspberry Pi with silver band facing the HDMI port. Connect mouse and keyboard using USB port. Connect HDMI with a screen.

Servos:
There are 3 wires connected to each servo (red/black/yellow) each representing power/ground/signal. Red should go directly into an external battery, black should go to ground on breadboard (which is the common ground for all batteries and servos.
