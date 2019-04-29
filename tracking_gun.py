import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import io
import time
import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
import RPi.GPIO as GPIO

def SetXAngle(angle):
    duty = angle
    GPIO.output(servo_x, True)
    pwm_x.ChangeDutyCycle(duty)
    time.sleep(1)
    # GPIO.output(servo_x, False)
    # pwm_x.ChangeDutyCycle(0)

def SetYAngle(angle):
    duty = angle
    GPIO.output(servo_y, True)
    pwm_y.ChangeDutyCycle(duty)
    time.sleep(1)
    # GPIO.output(servo_y, False)
    # pwm_y.ChangeDutyCycle(0)

def findCenter(maxW, maxX, maxY, maxH):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if len(faces) > 1:
            if w > maxW:
                maxW = w
                maxX = x
                maxY = y
                maxH = h
        else:
            maxW = w
            maxX = x
            maxY = y
            maxH = h

        midX = maxX+maxW/2
        midY = maxY+maxH/2
        center = (midX, midY)
        return center

def PullTrigger():
    release = 20/18+1
    pull = 160/18+1
    GPIO.output(servo_t, True)
    pwm_t.ChangeDutyCycle(release)
    time.sleep(1)
    GPIO.output(servo_t, True)
    pwm_t.ChangeDutyCycle(pull)
    time.sleep(1)
    GPIO.output(servo_t, True)
    pwm_t.ChangeDutyCycle(release)
    time.sleep(1)

def checkTarget():
    if (280 <= midX <= 360 and 200 <= midY <= 280):
        print 'target in range, FIRE!\n'
        print 're-calibrating...\n'
        PullTrigger()
        time.sleep(5)

def checkX(x_angle):
    # left 0
    # left of screen (< 300) -> left of gun -> want to turn left -> decrease x_angle
    print 'in checkX, x_angle = %f' % x_angle
    if (midX < 300):
        if (x_angle > 2.5):
            x_angle -= 0.5
            print 'move right'
        else:
            x_angle = 6.5
            print 'can\'t go left any more'
            print 're-calibrating...'
        return x_angle
    # right of screen (> 340) -> right of gun -> want to turn right -> increase x_angle
    elif (midX > 340):
        if (x_angle < 10.5):
            x_angle += 0.25
            print 'move right'
        else:
            x_angle = 6.5
            print 'can\'t go right any more'
            print 're-calibrating...'
        return x_angle
    return x_angle

def checkY(y_angle):
    # ceiling -> 0
    if (midY < 220):
        if (y_angle > 6.5):
            y_angle -= 0.25
            print 'move up'
        else:
            y_angle = 7.25
            print 'can\'t go down any more'
            print 're-calibrating...'
        return y_angle
    elif (midY > 260):
        if (y_angle < 8.5):
            y_angle += 0.5
            print 'move down'
        else:
            y_angle = 7.25
            print 'can\'t go up any more'
            print 're-calibrating...'
        return y_angle
    return y_angle

def initialize():
    SetYAngle(12.5)
    SetYAngle(2.5)
    SetYAngle(y_angle)
    SetXAngle(2.5)
    SetXAngle(12.5)
    SetXAngle(x_angle)
# global var
# servo pins
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
servo_x = 11
servo_y = 5
servo_t = 3
frequency = 50
x_angle = 7.5
y_angle = 6.5

try:

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_x, GPIO.OUT)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_y, GPIO.OUT)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_t, GPIO.OUT)

    pwm_x = GPIO.PWM(servo_x, frequency)
    pwm_y = GPIO.PWM(servo_y, frequency)
    pwm_t = GPIO.PWM(servo_t, frequency)

    pwm_x.start(0)
    time.sleep(1)
    pwm_y.start(0)
    time.sleep(1)
    pwm_t.start(0)
    time.sleep(1)

    # calibrate x and y servos and set them to x_angle, y_angle
    initialize()

    # initialize the camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # values of face capture
    maxX = 0; maxW = 0; maxY = 0; maxH = 0;
    reset = 1
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = gray[50:430, 100:540]
        # print len(gray), len(gray[0])
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60,60),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # find center
        center = None
        center = findCenter(maxW, maxX, maxY, maxH)

        if center:
            midX = center[0]
            midY = center[1]
            print '(midX, midY) = (%i, %i)\n' % (midX, midY)
            # check if it's on target
            checkTarget()
            # check x-axis
            x_angle = checkX(x_angle)
            SetXAngle(x_angle)
            # check y-axis
            y_angle = checkY(y_angle)
            SetYAngle(y_angle)
            print '(x_angle, y_angle) = (%f, %f)\n' % (x_angle, y_angle)
        else:
            # re-calibrate to initial position if no objects found in 30 iter
            if (reset % 30 == 0):
                initialize()
            print 'nothing detected'
            reset += 1

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            pwm_x.stop()
            pwm_y.stop()
            pwm_t.stop()
            GPIO.cleanup()
            break
        rawCapture.truncate(0)

# make sure program exits properly
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    pwm_x.stop()
    pwm_y.stop()
    pwm_t.stop()
    GPIO.cleanup()
finally:
    cv2.destroyAllWindows()
    pwm_x.stop()
    pwm_y.stop()
    pwm_t.stop()
    GPIO.cleanup()