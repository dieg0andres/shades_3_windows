import init
import time

from config import OPEN, CLOSED, UP, DOWN, NUMBER_OF_CALIBRATING_CYCLES

import uasyncio as asyncio



def calibration_constants():
    
    left_shade, middle_shade, right_shade = init.initialize_shades()

    # left shade
    #left_shade.set_time_to_close(9.81)
    #left_shade.set_time_to_open(11.81)
    
    #left_shade.set_mid_to_top_timing(5.41)
    #left_shade.set_top_to_mid_timing(5.01)
    
    #left_shade.set_mid_to_bottom_timing(5.01)
    #left_shade.set_bottom_to_mid_timing(6.01)
 
    left_shade.set_position(OPEN)

    #print(left_shade.get_time_to_close())
    #print(left_shade.get_time_to_open())

    #print(left_shade.get_mid_to_top_timing())
    #print(left_shade.get_top_to_mid_timing())
    
    #print(left_shade.get_mid_to_bottom_timing())
    #print(left_shade.get_bottom_to_mid_timing())
 
    print('left shade position: '+left_shade.get_position())
    
    
    # middle shade
    #middle_shade.set_time_to_close(9.81)
    #middle_shade.set_time_to_open(11.81)
    
    #middle_shade.set_mid_to_top_timing(5.41)
    #middle_shade.set_top_to_mid_timing(5.01)
    
    #middle_shade.set_mid_to_bottom_timing(5.01)
    #middle_shade.set_bottom_to_mid_timing(6.01)
 
    #middle_shade.set_position(OPEN)

    print(middle_shade.get_time_to_close())
    print(middle_shade.get_time_to_open())

    print(middle_shade.get_mid_to_top_timing())
    print(middle_shade.get_top_to_mid_timing())
    
    print(middle_shade.get_mid_to_bottom_timing())
    print(middle_shade.get_bottom_to_mid_timing())
 
    print(middle_shade.get_position())
    
    
    # right shade
    #right_shade.set_time_to_close(9.81)
    #right_shade.set_time_to_open(11.81)
    
    #right_shade.set_mid_to_top_timing(5.41)
    #right_shade.set_top_to_mid_timing(5.01)
    
    #right_shade.set_mid_to_bottom_timing(5.01)
    #right_shade.set_bottom_to_mid_timing(6.01)
 
    #right_shade.set_position(OPEN)

    print(right_shade.get_time_to_close())
    print(right_shade.get_time_to_open())

    print(right_shade.get_mid_to_top_timing())
    print(right_shade.get_top_to_mid_timing())
    
    print(right_shade.get_mid_to_bottom_timing())
    print(right_shade.get_bottom_to_mid_timing())
 
    print(right_shade.get_position())
    
    


# ------------------------------------------------------------------------------------------------#



def select_shade(left_shade, middle_shade, right_shade):
    
    print('\n\nThis is the calibration scrpt for the shades in the living room south side.')
    print('There are three shades: left_shade, middle_shade, right_shade')

    while True:
    
        print('\nWhich shade would you like to calibrate?')
        print('\n+ left_shade \n+ middle_shade \n+ right_shade')
        shade = input('\nMake your selection: ')

        if shade == 'left_shade':
            print('\nYou have selected '+shade)
            return left_shade

        if shade == 'middle_shade':
            print('\nYou have selected '+shade)
            return middle_shade

        if shade == 'right_shade':
            print('\nYou have selected '+shade)
            return right_shade


def select_element_for_calibration(): 

    print('\nWhat would you like to calibrate?')
    print('\n1) top to bottom timing AND bottom to top timing')
    print('2) top to mid timing AND mid to top timing')
    print('3) mid to bottom timing AND bottom to mid timing')
    print('4) shade position')
    
    while True:
    
        try: 
            command = int(input('\nMake a selection - 1, 2, 3, 4: '))
        
        except ValueError as ve:
            print('Enter an integer between 1 and 4')
        
        if command > 0 and command < 5:
            break

    return command


async def calibrate(element, shade):
    
    # top to bottom timing; time to close
    if element == 1:
        start_position = 'TOP'
        end_position = 'BOTTOM'
        await manually_move_shade_to_desired_position(start_position, shade)

        time_to_close, time_to_open = run_calibration_cycles_to_get_timings(start_position, end_position, shade)

        shade.set_time_to_close(time_to_close)
        shade.set_time_to_open(time_to_open)
        
        print('\nTimes saved:')
        print('time_to_close = '+ str(shade.get_time_to_close()))
        print('time_to_open = '+ str(shade.get_time_to_open()))

    # top to mid and mid to top
    elif element == 2:
        start_position = 'TOP'
        end_position = 'MID'
        await manually_move_shade_to_desired_position(start_position, shade)
        
        top_to_mid_timing, mid_to_top_timing = run_calibration_cycles_to_get_timings(start_position, end_position, shade)

        shade.set_top_to_mid_timing(top_to_mid_timing)
        shade.set_mid_to_top_timing(mid_to_top_timing)
        
        print('\nTimes saved:')
        print('top_to_mid_timing = '+ str(shade.get_top_to_mid_timing()))
        print('mid_to_top_timing = '+ str(shade.get_mid_to_top_timing()))
        
    # mid to bottom and bottom to mid
    elif element == 3:
        start_position = 'MID'
        end_position = 'BOTTOM'
        await manually_move_shade_to_desired_position(start_position, shade)
        
        mid_to_bottom_timing, bottom_to_mid_timing = run_calibration_cycles_to_get_timings(start_position, end_position, shade)

        shade.set_mid_to_bottom_timing(mid_to_bottom_timing)
        shade.set_bottom_to_mid_timing(bottom_to_mid_timing)
        
        print('\nTimes saved:')
        print('mid_to_bottom_timing = '+ str(shade.get_mid_to_bottom_timing()))
        print('bottom_to_mid_timing = '+ str(shade.get_bottom_to_mid_timing()))

    # set the position of the shade as "open"
    elif element == 4:
        
        desired_position = 'the top position- completely open position'
        await manually_move_shade_to_desired_position(desired_position, shade)
        shade.set_position(OPEN)
        print('\nShade position set as: '+shade.get_position())
        

def keep_going():
    ans = 0
    while True:
        try:
            print('\nWould you like to \n\n0) exit \n1) continue with calibration')
            ans = int(input('\nEnter your selection: '))
            break
            
        except ValueError as ve:
            print('enter "0" or "1"')
            
    return ans


def command_check(command):
    
    command = command.split()
    
    if len(command) != 2:
        return False
    
    if not( command[0] == UP or command[0] == DOWN ):
        return False
    
    try:
        command[1] = float( command[1] )
        
    except ValueError as ve:
        return False
    
    return True


async def manually_move_shade_to_desired_position(start_position, shade):
    
    finished = 0
    
    print('\nUsing commands "up x" and "down y", where x and y represent seconds (float),')
    print('manually move the shade to START POSITION:' + start_position)
        
    while True:
        command = input('\nEnter "up x" or "down x": ')
            
        if command_check(command):
                
            command = command.split()
                
            if command[0] == UP:
                await shade.motor.up(time_ = float(command[1]))
                
            if command[0] == DOWN:
                await shade.motor.down(time_ = float(command[1]))
                
            await asyncio.sleep(float(command[1])+ 1.0)
                
            while True:
         
                try:
                    print('\nIs shade at START POSITION: '+start_position+'? \n0 = No \n1 = Yes')
                    finished = int( input('Enter your selection: ') )
                    break
                    
                except ValueError as ve:
                    print('Enter 0 or 1')    
                
            if finished:
                break
    

def calibrate_via_script():
    
    print('\nTwo options to choose from to calibrate the shades in the living room south side:')
    print('\n1) calibrate via script or')
    print('2) calibrate via constants hardcoded in calibrate_helpers')
    
    while True:
        
        try:     
            command = int( input('\nMake your selection: '))
            if command == 1:
                return True
            if command == 2:
                return False
            else:
                print('\nTry again, enter option 1 or 2')
            
        except ValueError as ve:
            print('\nTry again, enter option 1 or 2')


def run_calibration_cycles_to_get_timings(start_position, end_position, shade):
    
    time_down = 0 # downward time
    time_up = 0 # upward time

    print('\nINSTRUCTIONS:\n')
    print('We will now move shade')
    print('     From START POSITION: '+start_position)
    print('     To END POSITION: '+end_position)
    print(str(NUMBER_OF_CALIBRATING_CYCLES)+' times and capture the average time it takes')
    print('\nPress 1 + ENTER to start moving shade and start timer')
    print('IMPORTANT: when shade gets to the END POSITION, press 0 + ENTER to stop timer AND MOTOR')
        
    while True:
        try:
            command = int( input('\nEnter 1 when ready to start...'))
            if command == 1:
                break
        except ValueError as ve:
            print('ERROR: Enter 1 when ready to start...')
        
    for i in range(NUMBER_OF_CALIBRATING_CYCLES):
            
        print('\nCycle '+str(i+1))
                    
        start = time.time()
        shade.motor.run_without_stop(DOWN)
        command = input('\nEnter 0 or anything to stop shade: ')
        shade.motor.stop()
        end = time.time()
        time_down = time_down + (end - start)
        print('That took: '+str(end-start)+' seconds')
            
        time.sleep(3)
            
        start = time.time()
        shade.motor.run_without_stop(UP)
        command = input('\nEnter 0 or anything to stop shade: ')
        shade.motor.stop()
        end = time.time()
        time_up = time_up + (end - start)
        print('That took: '+str(end-start)+' seconds')
            
        time.sleep(3)
    
    time_down = time_down / NUMBER_OF_CALIBRATING_CYCLES * 1.001
    time_up = time_up / NUMBER_OF_CALIBRATING_CYCLES * 1.001
  
    return time_down, time_up