from config import left_shade_pins, middle_shade_pins, right_shade_pins, motor_driver_pins, left_shade_file_names, middle_shade_file_names, right_shade_file_names, VCC, STBY, PWM, IN1, IN2
from controls import Motor_Driver, Shade



def initialize_shades():
    
    md = Motor_Driver( # vcc and STBY for motor module 1
        motor_driver_pins[VCC],
        motor_driver_pins[STBY]
        ) 
    
    md.activate()

    left_shade = Shade( #for s1 motor define pwm=20, in1=17, in2=16 ; s1 is the living room south side left shade
        left_shade_pins[PWM],
        left_shade_pins[IN1],
        left_shade_pins[IN2],
        left_shade_file_names
        ) 
    
    middle_shade = Shade( 
        middle_shade_pins[PWM],
        middle_shade_pins[IN1],
        middle_shade_pins[IN2],
        middle_shade_file_names
        ) 
    
    right_shade = Shade( 
        right_shade_pins[PWM],
        right_shade_pins[IN1],
        right_shade_pins[IN2],
        right_shade_file_names
        ) 

    return left_shade, middle_shade, right_shade