import uasyncio as asyncio
import time

from config import SSID, PSSWRD


def connect_to_network(wlan, led):
    wlan.active(True)
    wlan.connect(SSID, PSSWRD)

    # wait to connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed :(')
        led.on()
    else:
        print('Connected!')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        led.off()
        
        
async def heartbeat(led):
    led.on()
    await asyncio.sleep(0.2)
    led.off()
    await asyncio.sleep(7)
        

