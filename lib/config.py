# Home web server ip address
HOME_SERVER = 'http://192.168.86.32:8080'

# shades
LEFT_SHADE = 'left_shade'
MIDDLE_SHADE = 'middle_shade'
RIGHT_SHADE = 'right_shade'
ALL_SHADES = 'all_shade'

# get request command
MOVE_SHADE = '/move_shade'

# Shade positions
OPEN = "open"
CLOSED = "closed"
MID = "mid"

# Motor directions
UP = "up"
DOWN = "down"

# Pins
VCC = "vcc"
STBY = "STBY"
PWM = "pwm"
PWM_C = "pwm"
IN1 = "in1"
IN2 = "in2"
LED ="LED"

NUMBER_OF_CALIBRATING_CYCLES = 2


left_shade_file_names = {
        "position" : "/data/left_shade_position.bin",
        "time_to_open" : "/data/left_shade_time_to_open.bin",
        "time_to_close" : "/data/left_shade_time_to_close.bin",
        "mid_to_top_timing" : "/data/left_shade_mid_to_top_timing.bin",
        "top_to_mid_timing" : "/data/left_shade_top_to_mid_timing.bin",
        "mid_to_bottom_timing" : "/data/left_shade_mid_to_bottom_timing.bin",
        "bottom_to_mid_timing" : "/data/left_shade_bottom_to_mid_timing.bin"
    }


middle_shade_file_names = {
        "position" : "/data/middle_shade_position.bin",
        "time_to_open" : "/data/middle_shade_time_to_open.bin",
        "time_to_close" : "/data/middle_shade_time_to_close.bin",
        "mid_to_top_timing" : "/data/middle_shade_mid_to_top_timing.bin",
        "top_to_mid_timing" : "/data/middle_shade_top_to_mid_timing.bin",
        "mid_to_bottom_timing" : "/data/middle_shade_mid_to_bottom_timing.bin",
        "bottom_to_mid_timing" : "/data/middle_shade_bottom_to_mid_timing.bin"
    }


right_shade_file_names = {
        "position" : "/data/right_shade_position.bin",
        "time_to_open" : "/data/right_shade_time_to_open.bin",
        "time_to_close" : "/data/right_shade_time_to_close.bin",
        "mid_to_top_timing" : "/data/right_shade_mid_to_top_timing.bin",
        "top_to_mid_timing" : "/data/right_shade_top_to_mid_timing.bin",
        "mid_to_bottom_timing" : "/data/right_shade_mid_to_bottom_timing.bin",
        "bottom_to_mid_timing" : "/data/right_shade_bottom_to_mid_timing.bin"
    }

# GPIO pins
left_shade_pins = {
        "pwm" : 20,
        "in1" : 17,
        "in2" : 16
    }


middle_shade_pins = {
        "pwm" : 26,
        "in1" : 22,
        "in2" : 21
    }


right_shade_pins = {
        "pwm" : 13,
        "in1" : 14,
        "in2" : 15
    }


motor_driver_pins = {
        "vcc" : 19,
        "STBY" : 18
    }
