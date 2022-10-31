import init
import network
import socket
import time
import uasyncio as asyncio

from config import *
from controls import move_shade_to
from machine import Pin
from main_helpers import *


led = Pin(LED, Pin.OUT, 0)

wlan = network.WLAN(network.STA_IF)

left_shade, middle_shade, right_shade = init.initialize_shades()


async def serve_client(reader, writer):
    
    print('\nClient connected')
    
    request_line = await reader.readline()
    print('\nRequest: ', request_line)
    
    # We are not interested in HTTP requests headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line)
    print('explore: ', request.find(MOVE_SHADE))
    
    command = request.find(MOVE_SHADE) # command will equal '6' if the request has '/move_shade' in it
    
    if command == 6: # command is to move_shade

        shade = request.split(' ')[1].split('/')[2] # which is the shade to move (left_shade, middle_shade, right_shade)
        position = request.split(' ')[1].split('/')[3] # to which position (open, closed, mid)

        shades = [left_shade, middle_shade, right_shade]
        await move_shade_to(shade, position, shades)
    
    response = 'success' 
    
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)    
    
    await writer.drain()
    await writer.wait_closed()
    print('Client disconnected')


async def main():
    print('Connecting to WiFi Network...')
    connect_to_network(wlan, led)
    
    print('\nSetting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, '0.0.0.0',8080))
    
    while True:
        await heartbeat(led)
        

try:
    set_up_timers()
    asyncio.run(main())

finally:
    asyncio.create_task(log_request('in_finally_statement_of_main.py'))
    asyncio.new_event_loop()
    print('End of "finally" statement')

