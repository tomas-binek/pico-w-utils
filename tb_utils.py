from machine import Pin
import network
import time

class WiFi:
    def __init__(self, ssid: str, psk: str):
        self.ssid = ssid
        self.psk = psk
        self.wlan = network.WLAN(network.STA_IF)
        
    def connect(self, connectionTimeoutInSeconds: int, led = None):
        elapsedSeconds = 0
        checkIntervalInSeconds = 1
        
        while True:
            if (elapsedSeconds >= connectionTimeoutInSeconds):
                raise Exception("Timeout after %i seconds when connecting to network '%s'" % (connectionTimeoutInSeconds, self.ssid))
            
            self.wlan.active(True)
            self.wlan.connect(self.ssid, self.psk)
            
            for _ in range(0, 10):
                if self.wlan.status() == 3:
                    return
                
                elapsedSeconds += checkIntervalInSeconds
                time.sleep(checkIntervalInSeconds)
                
            self.wlan.disconnect()
            
            if led:
                led.blink(50, 100, 3)

class LedOnPin:
    def __init__(self, pinSpec):
        self.pin = Pin(pinSpec, Pin.OUT)
    
    def on(self):
        self.pin.value(1)
        
    def off(self):
        self.pin.value(0)
        
    def blink(self, onTimeMs: int, offTimeMs: int, repeat: int = None):
        if repeat is None or repeat == 0:
            self.on()
            time.sleep(onTimeMs / 1000)
            self.off()
            time.sleep(offTimeMs / 1000)
        #
        elif repeat == -1:
            while True:
                self.blink(onTimeMs, offTimeMs)
        else:
            for _ in range(0, repeat, 1):
                self.blink(onTimeMs, offTimeMs)
      
class RelayOnPin:
    def __init__(self, pinSpec):
        self.pin = Pin(pinSpec, Pin.OUT)
    
    def on(self):
        self.pin.value(0)
        
    def off(self):
        self.pin.value(1)