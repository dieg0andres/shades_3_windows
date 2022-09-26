from controls import Motor_Driver, Shade

import config
import init
import time

left_shade, middle_shade, right_shade = init.initialize_shades()


left_shade.set_time_to_close(9.625)
left_shade.set_time_to_open(13.75)

time.sleep(3)

print(left_shade.get_time_to_close())
print(left_shade.get_time_to_open())

#shade_left.set_position("open")

#for i in range(3):
#    shade_left.close_()
#    time.sleep(3)
#    shade_left.open_()
#    time.sleep(3)
