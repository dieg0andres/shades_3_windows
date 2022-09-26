from calibrate_helpers import calibration_constants, select_shade, select_element_for_calibration, calibrate, keep_going, calibrate_via_script
from init import initialize_shades

import uasyncio as asyncio

async def main():
    
    left_shade, middle_shade, right_shade = initialize_shades()
    print(middle_shade.motor.pwm, middle_shade.motor.in1, middle_shade.motor.in2)

    while True:
                
        if calibrate_via_script():   
            shade = select_shade(left_shade, middle_shade, right_shade)
            element = select_element_for_calibration()
            await calibrate(element, shade)
                
            if not keep_going():
                break
                
        else:
            print('\nInstructions: go to calibrate_helpers.py file and edit the values in the calibration_constants() function')
            print('Do not forget to save the file')
            input('\nWhen done press any key and shades will calibrate: ')
                    
            calibration_constants()
                    
            break

asyncio.run(main())