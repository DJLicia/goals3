#!/usr/bin/env python3
#
#   drive.py
#
#   Goals 2. Drive system class, line sensor class

import pigpio
import sys
import time
import traceback
import motor

# Motor = motor.Motor()
# IR = motor.IR()

class Drive_System:
    def __init__(self, io, motorL_pinA, motorL_pinB, motorR_pinA, motorR_pinB):
        self.motorL = motor.Motor(io, motorL_pinA, motorL_pinB)
        self.motorR = motor.Motor(io, motorR_pinA, motorR_pinB)
    
    def stop(self):
        self.motorL.stop()
        self.motorR.stop()
        
    
    def steering(self, power1, power2):
        self.motorL.setlevel(power1)
        self.motorR.setlevel(power2) 
    
    def drive(self, side, turn_radius):
        if side == "s" and turn_radius == "straight":
            self.steering(0.74, 0.76)
        elif side == "l" and turn_radius == "veer":
            self.steering(0.70, 0.85)
        elif side == "l" and turn_radius == "steer":
            self.steering(0.65, 0.87)
        elif side == "l" and turn_radius == "turn":
            self.steering(0.55, 0.90)
        elif side == "l" and turn_radius == "hook":
            self.steering(0.5, 0.95)
        elif side == "l" and turn_radius == "spin":
            self.steering(-0.60, 0.60)
        elif side == "r" and turn_radius == "veer":
            self.steering(0.85, 0.70)
        elif side == "r" and turn_radius == "steer":
            self.steering(0.87, 0.65)
        elif side == "r" and turn_radius == "turn":
            self.steering(0.90, 0.55)
        elif side == "r" and turn_radius == "hook":
            self.steering(0.95, 0.5)
        elif side == "r" and turn_radius == "spin":
            self.steering(0.60, -0.60)
        
        
class Line_Sensor:
    def __init__(self, io, IR_pin_left, IR_pin_mid, IR_pin_right):
        self.IR_pin_L = motor.IR(io, IR_pin_left)
        self.IR_pin_M = motor.IR(io, IR_pin_mid)
        self.IR_pin_R = motor.IR(io, IR_pin_right)

    
    def read_line(self):
        irl = self.IR_pin_L.read()
        irm = self.IR_pin_M.read()
        irr = self.IR_pin_R.read()
        return (irl, irm, irr)
    
