#!/usr/bin/python3

import datetime
import os

import bme280
import boto3
import smbus2
from dotenv import main as dotenv

dotenv.load_dotenv()

s3_access_key = os.environ.get('S3ACCESSKEY')
s3_secret_key = os.environ.get('S3SECRETKEY')
location = os.environ.get('LOCATION')

port = 1
address = 0x76
bus = smbus2.SMBus(port)

filename = f'{location}-{datetime.datetime.now().strftime("%Y%m%d")}.csv'
targetdir = f'{os.path.dirname(os.path.abspath(__file__))}/data'
target = f'{targetdir}/{filename}'

bme280.load_calibration_params(bus, address)

if not os.path.exists(target):
    if not os.path.exists(targetdir):
        os.mkdir(targetdir)
    with open(target, "a") as f:
        f.write("timestamp,temp,humidity,airpressure\n")

with open(target, "a+") as f:
    bme280_data = bme280.sample(bus, address)
    timenow = bme280_data.timestamp.astimezone().strftime('%Y/%m/%d-%H:%M:%S')
    ambient_temperature = bme280_data.temperature
    humidity = bme280_data.humidity
    pressure = bme280_data.pressure
    f.write(f"{timenow},{ambient_temperature},{humidity},{pressure}\n")

with open(file=target, mode='rb') as f:
    bucket_name = 'tsutsui-test'
    s3 = boto3.client(
        "s3", aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key
    )

    s3.put_object(Bucket=bucket_name, Body=f, Key=filename)
