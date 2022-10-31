import time
import uasyncio as asyncio
import urequests as requests

from config import *
from machine import Timer
from private import SSID, PSSWRD


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
        
    asyncio.create_task(log_request('Connected_to_WiFi'))
    asyncio.create_task(log_request(status[0]))
    asyncio.create_task(send_ip(status[0]))


async def heartbeat(led):
    led.on()
    await asyncio.sleep(0.2)
    led.off()
    await asyncio.sleep(7)
    
    
async def log_request(msg):
    r = requests.get(HOME_SERVER + '/log/LIVING_ROOM_SOUTH/'+msg)
    r.close()
    print('sent log request, message = ', msg)


def reset_pico_cb(timer):
    machine.reset()


async def send_ip(ip):
    r = requests.get(HOME_SERVER + '/ip/LIVING_ROOM_SOUTH/' + ip)
    r.close()
    print('sent ip', ip)
    
    
def set_up_timers():
    reset_timer = Timer()
    send_ip_timer = Timer()
    
    reset_timer.init(period=1*1000*60*60*24, mode=Timer.PERIODIC, callback=reset_pico_cb)
    #send_ip_timer.init(period=15000, mode=Timer.PERIODIC, callback=send_ip_cb)
    