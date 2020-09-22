# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
import network
import uos
import machine
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
# webrepl.start()
gc.collect()

# disable access point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
