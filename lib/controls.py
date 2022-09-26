import time
import uasyncio as asyncio

from config import OPEN, MID, CLOSED, UP, DOWN, PWM_C, IN1, IN2, LEFT_SHADE, MIDDLE_SHADE, RIGHT_SHADE, ALL_SHADES # Shade positions, motor directions, and Pins
from machine import Pin, PWM


# main purpose of Motor_Driver class is to define and control the Vcc and STBY pins of the TB6612FNG board
class Motor_Driver:
    
    def __init__(self, vcc, STBY):
        self.vcc = Pin(vcc, Pin.OUT, value=0)
        self.STBY = Pin(STBY, Pin.OUT, value=0)
    
    def activate(self):
        self.vcc.on()
        self.STBY.on()
            
    def deactivate():
        self.vcc.off()
        self.STBY.off()
            
    def standby():
        self.STBY.off()
            
    def wakeup():
        self.STBY.on()



class Motor:
    
    # to create a motor pass in the GPIO pins for pwm, in1, and in2 (TB6612FNG)
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            
            if key == PWM_C:
                self.pwm = PWM(Pin(value))
                self.pwm.freq(1000)
                self.pwm.duty_u16(0)
            
            if key == IN1:
                self.in1 = Pin(value, Pin.OUT, value=0)
            
            if key == IN2:
                self.in2 = Pin(value, Pin.OUT, value=0)


    async def up(self, **kwargs):
        asyncio.create_task(self._run(UP, **kwargs))
        
                   
    async def down(self, **kwargs):        
        asyncio.create_task(self._run(DOWN, **kwargs))
        
        
    async def _run(self, direction, **kwargs):
        
        time_ = 1 # run motor for 1 sec unless a differnt value is passed in **kwargs
        speed = 100 # run motor at max speed unless a different value is passed in **kwargs
        
        for key, value in kwargs.items():
            
            if key == "time_":
                time_ = value
            if key == "speed":
                speed = value
        
        self.pwm.duty_u16( int(speed/100 * 65535) )

        if direction == UP:
            self.in1.on()
            self.in2.off()
            
        if direction == DOWN:
            self.in1.off()
            self.in2.on()
            
        await asyncio.sleep(time_)
        
        self.stop()

    
    def stop(self):
        self.in1.off()
        self.in2.off()
        self.pwm.duty_u16(0)
  
  
    def run_without_stop(self, direction):
        
        self.pwm.duty_u16( 65535 )

        if direction == UP:
            self.in1.on()
            self.in2.off()
            
        if direction == DOWN:
            self.in1.off()
            self.in2.on()



class Shade:
    
    def __init__(self, pwm, in1, in2, file_names):
        
        self.position_file = file_names["position"]
        
        self.time_to_open_file = file_names["time_to_open"]
        self.time_to_close_file = file_names["time_to_close"]
        
        self.mid_to_top_timing_file = file_names["mid_to_top_timing"]
        self.top_to_mid_timing_file = file_names["top_to_mid_timing"]
        
        self.mid_to_bottom_timing_file = file_names["mid_to_bottom_timing"]
        self.bottom_to_mid_timing_file = file_names["bottom_to_mid_timing"]
        
        self.motor = Motor(pwm=pwm, in1=in1, in2=in2)
        
    # moves Shade to 100% open
    def open_(self):
        
        position = self.get_position()
        
        if position == OPEN:
            pass # do nothing
        
        elif position == CLOSED:
            await self.motor.up(time_= self.get_time_to_open())
            self.set_position(OPEN)
            
        elif position == MID:
            await self.motor.up(time_= self.get_mid_to_top_timing())
            self.set_position(OPEN)
    
    # moves Shade to 0% open
    async def close_(self):
        
        position = self.get_position()
        
        if position == OPEN:
            await self.motor.down(time_= self.get_time_to_close())
            self.set_position(CLOSED)
            
        elif position == CLOSED:
            pass # do nothing
        
        elif position == MID:
            await self.motor.down(time_= self.get_mid_to_bottom_timing())
            self.set_position(CLOSED)
            
    
    async def go_to_mid(self):
        
        position = self.get_position()
        
        if position == OPEN:
            await self.motor.down(time_= self.get_top_to_mid_timing())
            self.set_position(MID)
            
        elif position == CLOSED:
            await self.motor.up(time_= self.get_bottom_to_mid_timing())
            self.set_position(MID)
        
        elif position == MID:
            pass # do nothing
    
    
    def get_position(self):
        return self._read_from_file(self.position_file)
    
 
    def set_position(self, position):
        self._write_to_file(position, self.position_file)
  
  
    def get_time_to_open(self):
        return float( self._read_from_file(self.time_to_open_file) )
        
  
    def set_time_to_open(self, time_to_open):
        self._write_to_file(time_to_open, self.time_to_open_file)
    
    
    def get_time_to_close(self):
        return float( self._read_from_file(self.time_to_close_file) )
   
   
    def set_time_to_close(self, time_to_close):
        self._write_to_file(time_to_close, self.time_to_close_file)
        
        
    def get_mid_to_top_timing(self):
        return float( self._read_from_file(self.mid_to_top_timing_file) )
    
    
    def set_mid_to_top_timing(self, mid_to_top_timing):
        self._write_to_file(mid_to_top_timing, self.mid_to_top_timing_file)
        
      
    def get_top_to_mid_timing(self):
        return float( self._read_from_file(self.top_to_mid_timing_file) )
    
    
    def set_top_to_mid_timing(self, top_to_mid_timing):
        self._write_to_file(top_to_mid_timing, self.top_to_mid_timing_file)      

        
    def get_mid_to_bottom_timing(self):
        return float( self._read_from_file( self.mid_to_bottom_timing_file ) )
    
    
    def set_mid_to_bottom_timing(self, mid_to_bottom_timing):
        self._write_to_file( mid_to_bottom_timing, self.mid_to_bottom_timing_file )
    
    
    def get_bottom_to_mid_timing(self):
        return float( self._read_from_file( self.bottom_to_mid_timing_file ) )
    
    
    def set_bottom_to_mid_timing(self, bottom_to_mid_timing):
        self._write_to_file(bottom_to_mid_timing, self.bottom_to_mid_timing_file)
      
      
    def _write_to_file(self, data, file_name):
        file = open(file_name, 'w')
        file.write(str(data))
        file.close()
    
    
    def _read_from_file(self, file_name):
        file = open(file_name, 'r')
        data = file.read()
        file.close()
        return data
    
# used in main.py    
async def move_shade_to(shade, position, shades):
    print('\nMove shade: '+shade)
    print('To position: '+ position)
    
    left_shade = shades[0]
    middle_shade = shades[1]
    right_shade = shades[2]
    
    if shade == LEFT_SHADE:
        if position == OPEN:
            await left_shade.open_()
        if position == CLOSED:
            await left_shade.close_()
        if position == MID:
            await left_shade.go_to_mid()
    
    elif shade == MIDDLE_SHADE:
        if position == OPEN:
            await middle_shade.open_()
        if position == CLOSED:
            await middle_shade.close_()
        if position == MID:
            await middle_shade.go_to_mid()
        
    elif shade == RIGHT_SHADE:
        if position == OPEN:
            await right_shade.open_()
        if position == CLOSED:
            await right_shade.close_()
        if position == MID:
            await right_shade.go_to_mid()
        
    elif shade == ALL_SHADES:
        if position == OPEN:
            await left_shade.open_()
            await middle_shade.open_()
            await right_shade.open_()
        if position == CLOSED:
            await left_shade.close_()
            await middle_shade.close_()
            await right_shade.close_()
        if position == MID:
            await left_shade.go_to_mid()
            await middle_shade.go_to_mid()
            await right_shade.go_to_mid()