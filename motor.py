#!/usr/bin/env python3
#
#   motor.py
#
#   Goals 1. Code to control a motor. 
#   Goals 2. Code to use IR sensors

# Imports
import pigpio
import sys
import time
import traceback

class Motor:
    
    def __init__(self, io, pin1, pin2):
        #TODO: What arguments to pass?
        
        # Define the motor pins.
        self.PIN_MOTOR_LEGA = pin1
        self.PIN_MOTOR_LEGB = pin2
        self.io = io
    
        # Set up the four pins as output (commanding the motors).
        self.io.set_mode(self.PIN_MOTOR_LEGA, pigpio.OUTPUT)
        self.io.set_mode(self.PIN_MOTOR_LEGB, pigpio.OUTPUT)
        
        # Set the PWM frequency to 1000Hz.
        self.io.set_PWM_frequency(self.PIN_MOTOR_LEGA, 1000)
        self.io.set_PWM_frequency(self.PIN_MOTOR_LEGB, 1000)
        
        # Clear all pins, just in case.
        self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGA, 0)
        self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGB, 0)

    def stop(self):
        #TODO: how to halt motor
        
        # Clear all pins, just in case.
        self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGA, 0)
        self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGB, 0)

    def setlevel(self, level):
        #TODO: sets level in the range -1.0 --- 1.0, relative to max motor power
        if -1.0 <= level < 0:
            self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGA, -1 * 255 * level)
            self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGB, 0)
        if 0 < level <= 1.0:
            self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGB, 255 * level)
            self.io.set_PWM_dutycycle(self.PIN_MOTOR_LEGA, 0)
            # ytp;ppyt-+tr lololool

class IR:    
    def __init__(self, io, IR_pin):
        self.PIN_IR = IR_pin
        self.io = io
        self.io.set_mode(self.PIN_IR,   pigpio.INPUT)
    
    def read(self):
        # print(io.read(self.PIN_IR))

        return self.io.read(self.PIN_IR)

            
if __name__ == "__main__":
    #TODO: instantiate I/O object, instantiate two motor objects (L/R),
    # program behaviors, stop motors and I/O before exiting
    
    # Prepare the GPIO interface/connection (to command the motors).
    print("Setting up the GPIO...")
    io = pigpio.pi()
    if not io.connected:
        print("Unable to connection to pigpio daemon!")
        sys.exit(0)
    print("GPIO ready...")
    
    motorL_pinA = 8
    motorL_pinB = 7
    # make sure to double check rasbpi mapping for motors
    motorR_pinA = 6
    motorR_pinB = 5

    pin_IR_left = 14
    # change numbers when we actually link them
    pin_IR_middle = 15
    pin_IR_right = 18

    motorL = Motor(io, motorL_pinA, motorL_pinB)
    motorR = Motor(io, motorR_pinA, motorR_pinB)

    IR_left = IR(io, pin_IR_left)
    IR_middle = IR(io, pin_IR_middle)
    IR_right = IR(io, pin_IR_right)
    
    try:
        # Example: Continually read and report all three pins.
        while True:
            irl = IR_left.read()
            irm = IR_middle.read()
            irr = IR_right.read()
        
            print("IRs: L %d  M %d  R %d" % (irl, irm, irr))

    except BaseException as ex:
        # Report the error, then continue with the normal shutdown.
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()


    ############################################################
    # Turn Off.
    # Nothing to do for the sensors.
    print("Turning off...")    
    # for i in range(4):
    #     # forward , use setlevel 
    #     motorL.setlevel(0.72)
    #     motorR.setlevel(0.70)
    #     time.sleep(3.6)
        
    #     #stop
    #     motorL.stop()
    #     motorR.stop()
    #     time.sleep(1)
        
    #     # turn right by running Left forward and Right backwards
    #     motorL.setlevel(0.75)
    #     motorR.setlevel(-0.75)
    #     time.sleep(0.73)
        
    #     # stop
    #     motorL.stop()
    #     motorR.stop()
    #     time.sleep(1)
    
    io.stop()