#!/usr/bin/env python3
#
#   drive.py
#
#   Goals 2. Flower power function, and line-following function

import pigpio
import sys
import time
import traceback

import motor
import drive

# Motor = motor.Motor()
# IR = motor.IR()

def flower_power(driver):
    # loop through 11 options ???
    for i in range(11):
        # two for lopps for two lists of directions
        if i == 0:
            driver.drive("s", "straight")
            time.sleep(3.5)
            driver.stop()
            time.sleep(4.0)
        elif i == 1:
            driver.drive("l", "veer")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 2:
            driver.drive("l", "steer")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 3:
            driver.drive("l", "turn")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 4:
            driver.drive("l", "hook")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 5:
            driver.drive("l", "spin")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 6:
            driver.drive("r", "veer")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 7:
            driver.drive("r", "steer")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 8:
            driver.drive("r", "turn")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 9:
            driver.drive("r", "hook")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)
        elif i == 10:
            driver.drive("r", "spin")
            time.sleep(3.0)
            driver.stop()
            time.sleep(4.0)

    driver.stop()
    input("hit return")

# Makes robot go forward for intersection
def pull_forward(driver):
    t_last = 0.0
    t_0 = time.time()
    while(True):
        t_now = time.time()
        
        if t_now < t_0 + 0.4:
            driver.drive("s", "straight")
            #print("pulling forward")
        else:
            driver.stop()
        if t_now > t_0 + 0.4 + 0.1:
            driver.stop()
            break 

# -1 to 1
SIDE_RAW_DICT = {(0, 0, 0): 0.0, (1, 1, 1): 0.0, (0, 1, 0): 0.0, 
(0, 1, 1): -0.5, (0, 0, 1): -1.,
(1, 1, 0): 0.5, (1, 0, 0): 1. , (1, 0, 1): 0.0}

def new_street_turn(driver, sensor, direction):
    t_const = 0.2
    turn_lvl = 0
    t_last = time.time()
    raw = 0.0
    on_old_line = True
    # print("Turning")
    t1 = time.time()
    while(True):
        t_now = time.time()
        dt = t_now - t_last
        t_last = t_now
        line_reading = sensor.read_line()
        if direction == '1':
            # on_old_line = False
            #print("SPIN GODAMNIT")
            driver.drive("l", "spin")
        elif direction == '2':
            # on_old_line = False
            driver.drive("r", "spin")
        if line_reading == (0, 0, 0):
            on_old_line = False
        if not on_old_line:
            if line_reading == (0, 1, 0):
                raw = 0.6
                # on_old_line = True
            if line_reading == (0, 1, 1) or line_reading == (1, 1, 0):
                raw = 1.0
            elif line_reading == (0, 0, 1) or line_reading == (1, 0, 0):
                raw = 0.7 #should flip this with threshold
            else:
                raw = 0.0
        turn_lvl = turn_lvl + (dt / t_const) * (raw - turn_lvl)
        # print("Turn_lvl: ", turn_lvl)
        # print("On line: ", on_old_line)
        #need to change this such that it accounts for the case where it is still on a street and turns onto a different one
        if turn_lvl > 0.4 and (not on_old_line):
            driver.stop()
            t2 = time.time()
            print("Time to turn: ", t2 - t1, "sec" )
            break
    
def line_follower(driver, sensor):
    # black = 1
    # white/none = 0
    t_const = 0.2
    direction = 2
    SIDE_STATE = 0
    # Intersection detection
    intr_level = 0.0
    intr_raw = 0.0
    t_intr = 0.2
    t_end_const = 0.01

    # Side Detection
    side_lvl = 0.0
    side_raw = 0.0
    t_side_const = 0.01

    # End Detection
    end_lvl = 0.0
    end_raw = 0.0

    t_last = 0.0
    print("Now line following")
    while(True):
        line_reading = sensor.read_line()
        t_now = time.time()
        dt = t_now - t_last
        t_last = t_now

        # Intersection Raw Values
        if line_reading == ((1, 1, 1)):
            intr_raw = 1.0
        else:
            intr_raw = 0.0
        
        intr_level = intr_level + (dt / t_intr) * (intr_raw - intr_level)
        # check exit condition for intersection threshold
        if intr_level >= 0.5:
            driver.stop()
            break # brings us out of line following into main
        
        # side filter
        # get raw from dictionary 
        side_raw = SIDE_RAW_DICT.get(line_reading)
        #print("line reading: ", line_reading)
        if line_reading != (0, 0, 0):
            side_lvl = side_lvl + (dt / t_side_const) * (side_raw - side_lvl)
        # else:
        #     continue
        #print("side level: ", side_lvl)
        
        
        if side_lvl >= 0.8: # on the right
            SIDE_STATE = 1
        elif side_lvl > -0.2 and side_lvl < 0.2: # CENTERED
            SIDE_STATE = 0
        elif side_lvl <= -0.8:
            SIDE_STATE = -1

        # check exit condition for off line threshold
        #print("Side: ", SIDE_STATE)
        if SIDE_STATE == 0 and line_reading == ((0, 0, 0)):
            end_raw = 1.0 #fix this with threshold
        else:
            end_raw = 0.0
        
        # End Detection
        end_lvl = end_lvl + (dt / t_end_const) * (end_raw - end_lvl)
        #print("End lvl: ", end_lvl)
        
        if end_lvl >= 0.3:
            driver.stop()
            # if side_lvl >= 0.2 or side_lvl <= -0.2:
            #     #go back to line following
            #     continue
            break # want it to leave line follower function
        
        
        if line_reading == (0, 1, 0): # go straight
            driver.drive("s", "straight")
        elif line_reading == (0, 1, 1): # steer right
            driver.drive("r", "turn")
        elif line_reading == (0, 0, 1): # steer right
            driver.drive("r", "hook")
        elif line_reading == (0, 0, 0): # Off the line
            #print(side_lvl)
            if SIDE_STATE == -1:
                #end_raw = 0
                driver.drive("r", "hook")
            elif SIDE_STATE == 0:
                #end_raw = 1
                # driver.drive("s", "straight")
                driver.stop()
            elif SIDE_STATE == 1:
                #end_raw = 0
                driver.drive("l", "hook")
        elif line_reading == (1, 1, 0): # veer left
            driver.drive("l", "turn")
        elif line_reading == (1, 0, 0): # steer left
            driver.drive("l", "hook")

#
#   Main
#
if __name__ == "__main__":
    


    ############################################################
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

    #print("Sensors ready...")
    
    driver = drive.Drive_System(io, motorL_pinA, motorL_pinB, motorR_pinA, motorR_pinB)
    sensor = drive.Line_Sensor(io, pin_IR_left, pin_IR_middle, pin_IR_right)
    
    try:
        ''' Goals 3: dealing with angled intersections through filters ''' 
        while(True):
            line_follower(driver, sensor)
            print("Out of line follower")
            direction = input("Hit 1 for left, 2 for right ") 
            pull_forward(driver)
            
            t1 = time.time()
            new_street_turn(driver, sensor, direction)
            t2 = time.time()
            print("Turn time: ", t2 - t1, "sec")

    except BaseException as ex:
        # Report the error, then continue with the normal shutdown.
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()


    ############################################################
    # Turn Off.
    # Nothing to do for the sensors.
    print("Turning off...")

    # Also stop the interface.
    driver.stop()
    io.stop()