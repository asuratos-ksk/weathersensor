#!/usr/bin/python3

import datetime
import os

import bme280
import smbus2

port = 1
address = 0x76
bus = smbus2.SMBus(port)
filename = 'weatherdata'
currentdir = os.path.dirname(__file__)
target = f'{currentdir}/data/{filename}.csv'

bme280.load_calibration_params(bus, address)

if not os.path.exists(f'{currentdir}/data'):
    os.mkdir(f'{currentdir}/data')
    with open(target, "a") as f:
        f.write("timestamp,temp,humidity,airpressure\n")

with open(target, "a") as f:
    # timenow = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    bme280_data = bme280.sample(bus, address)
    timenow = bme280_data.timestamp.strftime('%Y/%m/%d-%H:%M:%S')
    ambient_temperature = bme280_data.temperature
    humidity = bme280_data.humidity
    pressure = bme280_data.pressure
    f.write(f"{timenow},{ambient_temperature},{humidity},{pressure}\n")
