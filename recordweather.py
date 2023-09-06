#!/usr/bin/python3

import datetime
import os

import bme280
import smbus2

# import time

port = 1
address = 0x76  # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)
filename = 'weatherdata'
currentdir = os.path.dirname(__file__)

bme280.load_calibration_params(bus, address)

target = f'{currentdir}/data/{filename}.csv'

if not os.path.exists(target):
    with open(target, "a") as f:
        f.write("timestamp,temp,humidity,airpressure\n")

with open(target, "a") as f:
    # while True:
    timenow = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    bme280_data = bme280.sample(bus, address)
    ambient_temperature = bme280_data.temperature
    humidity = bme280_data.humidity
    pressure = bme280_data.pressure
    # print(f"{timenow},{ambient_temperature},{humidity},{pressure}\n")
    # time.sleep(1)
    f.write(f"{timenow},{ambient_temperature},{humidity},{pressure}\n")
