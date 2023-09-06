#!/usr/bin/python3

import os

import bme280
import boto3
import smbus2
from dotenv import main as dotenv

dotenv.load_dotenv()

port = 1
address = 0x76
bus = smbus2.SMBus(port)
filename = 'weatherdata'
currentdir = os.path.dirname(__file__)
target = f'{currentdir}/data/{filename}.csv'

s3_access_key = os.environ.get('S3ACCESSKEY')
s3_secret_key = os.environ.get('S3SECRETKEY')

bme280.load_calibration_params(bus, address)

if not os.path.exists(f'{currentdir}/data'):
    os.mkdir(f'{currentdir}/data')
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

    s3.put_object(Bucket=bucket_name, Body=f, Key=os.environ.get('FILENAME'))
