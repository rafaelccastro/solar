from ina219 import INA219  # Importing necessary library to run INA219.
import time
import ntptime  # Importing ntptime for getting NTP time
import network  # Required to connect to Wi-Fi (if running on ESP8266/ESP32)
from machine import Pin, I2C  # Importing necessary libraries to run I2C.

# Connect to Wi-Fi (Modify with your Wi-Fi credentials)
SSID = 'Berkeley-IoT'
PASSWORD = '34i$I6x1'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected:", wlan.ifconfig())

# Connect to Wi-Fi before syncing NTP time
connect_wifi()

# Sync time with NTP server
try:
    ntptime.settime()
except:
    print("Failed to sync time with NTP server")

i2c1 = I2C(0, scl=Pin(8), sda=Pin(9), freq=100000)  # Creating I2C object with pins 8 and 9 for INA219.

SHUNT_OHMS = 0.1  # Shunt resistor value in ohms.
ina1 = INA219(SHUNT_OHMS, i2c1)  # Creating INA219 object with the shunt resistor value and I2C object.
ina1._address = 0x40
ina1.configure()  # Configuring INA219 object.

SHUNT_OHMS = 0.1  # Shunt resistor value in ohms.
ina2 = INA219(SHUNT_OHMS, i2c1)
ina2._address = 0x41
ina2.configure()


while True:  # Infinite loop to collect data.
    V1 = ina1.supply_voltage()  # Collecting bus voltage.
    I1 = ina1.current()  # Collecting current.
    P1 = ina1.power()  # Collecting power.

    if I1 > 0:
        R1 = V1 / (I1 / 1000)  # Calculating resistance.
    else:
        R1 = 0

  
    V2 = ina2.supply_voltage()  # Collecting bus voltage.
    I2 = ina2.current()  # Collecting current.
    P2 = ina2.power()  # Collecting power.

    if I2 > 0:
        R2 = V2 / (I2 / 1000)  # Calculating resistance.
    else:
        R2 = 0


    # Get the current timestamp from system time (which is now synced with NTP)
    timestamp = time.localtime(time.time() - 8 * 3600)
    time_str = f"{timestamp[0]}-{timestamp[1]:02d}-{timestamp[2]:02d} {timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d}"

    # Print CSV-formatted numeric data (without units)
    print(f"{time_str},{V1:.3f},{I1:.3f},{P1:.3f},{R1:.3f},{V2:.3f},{I2:.3f},{P2:.3f},{R2:.3f}")  

    time.sleep(0.5)  # Sleeping for 2 seconds.