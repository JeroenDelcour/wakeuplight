import machine
import network
import math
import time
from datetime_stuff import *

# status led is on during boot sequence, turns off after successful boot
status_led = machine.Pin(16, machine.Pin.OUT)
status_led.off()  # off means turning ON the LED in this case

# connect to wifi
with open("wifi.txt", "r") as f:
    ssid = f.readline().strip()
    password = f.readline().strip()
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print("Connecting to network...")
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(1)
print("Network config:", sta_if.ifconfig())

# get local time from World Time API
rtc = machine.RTC()
set_local_datetime(rtc)
print("Local time: {}".format(rtc.datetime()))
last_time_sync = current_epoch(rtc)

for i in range(rtc.datetime()[4]):
    status_led.on()
    time.sleep(0.5)
    status_led.off()
    time.sleep(0.1)


start = (6, 15)  # hours, minutes
duration = 30  # minutes
# LED strip is controlled by pin 12 (labeled D6 on board)
led = machine.PWM(machine.Pin(12), freq=1000)
led.duty(0)

# convert start to epoch time for next morning
start_epoch = list(rtc_datetime_to_time_datetime(rtc.datetime()))
start_epoch[3] = start[0]
start_epoch[4] = start[1]
start_epoch[5] = 0
start_epoch = time.mktime(tuple(start_epoch))
if start_epoch < current_epoch(rtc):
    # start time has already passed today, set it to tomorrow instead
    start_epoch += 24*60*60
duration_seconds = duration * 60

status_led.on()  # turn OFF status LED

while True:
    print(rtc.datetime())

    # sync internet time every hour
    if current_epoch(rtc) - last_time_sync > 1 * 60 * 60:
        print("Syncing time from World Time API")
        set_local_datetime(rtc)
        last_time_sync = current_epoch(rtc)

    intensity = (current_epoch(rtc) - start_epoch) / duration_seconds
    intensity = max(0, min(intensity, 1))
    intensity = intensity ** 3  # human perception of light intensity is logarithmic
    # print(time.localtime(), intensity)
    led.duty(int(intensity * 1024))
    time.sleep(1)
