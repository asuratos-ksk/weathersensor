import datetime
import os

# import bme280
# import smbus2

port = 1
address = 0x77  # Adafruit BME280 address. Other BME280s may be different
# bus = smbus2.SMBus(port)
filename = 'weatherdata'

# bme280.load_calibration_params(bus, address)

if not os.path.exists(f"data/{filename}.csv"):
    with open(f"data/{filename}.csv", "a") as f:
        f.write("timestamp,temp,humidity,airpressure\n")

with open(f"data/{filename}.csv", "a") as f:
    timenow = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    # bme280_data = bme280.sample(bus, address)
    # ambient_temperature = bme280_data.temperature
    # humidity = bme280_data.humidity
    # pressure = bme280_data.pressure
    f.write(f"{timenow}\n")
