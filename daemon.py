import time
import json
import kafka
import requests

from consts import *
from datetime import datetime
from kafka import KafkaProducer
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler

from metrics import get_acess_token
from metrics import parking_data, parking_format_influx
from metrics import wirelessUsers_data, wirelessUsers_format_influx

# jobs
def hour_job():
    print("this job runs every 1 hour")

def ten_sec_job(producer):
    pass

def thirty_sec_job():
    print("this job runs every 30 sec")

def twenty_min_job(producer, client, token, keys):
    # parking data
    parking = parking_data()
    keys["parking"] = keys["parking"] + 1
    producer.send("parking", value={"PARK"+str(keys["parking"]) : parking})

    # parking data influx formated
    parking = parking_format_influx(parking)


    # number of wireless users data
    wireless_users = wirelessUsers_data(token)
    print(wireless_users)
    keys["wirelessUsers"] = keys["wirelessUsers"] + 1
    producer.send("wifiusr", value={"WIFIUSR"+str(keys["wirelessUsers"]) : wireless_users})




def main():
    print("runs main")
    # start scheduler
    scheduler = BackgroundScheduler()
    
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)

    # start Kafka Python Client
    producer = KafkaProducer(bootstrap_servers=['13.69.49.187:9092'], value_serializer=lambda x: json.dumps(x, indent=4, sort_keys=True, default=str).encode('utf-8'))

    # start influxDBClient
    influx = InfluxDBClient(host='127.0.0.1', port=8086)

    # create influx user and database
    influx.create_user("daemon", "daemon_1234", admin=True)
    influx.create_database("Metrics")

    # get primecoreAPI access token
    token = get_acess_token()

    # add jobs
    scheduler.add_job(hour_job, trigger="interval", hours=1, id="1hourjob")
    scheduler.add_job(ten_sec_job, trigger="interval", args=[producer], seconds=10, id="10secjob")
    scheduler.add_job(thirty_sec_job, trigger="interval", seconds=30, id="30secjob")
    scheduler.add_job(twenty_min_job, trigger="interval", args=[producer, client, token, KAFKAKEYS], minutes=20, id="20minjob", next_run_time=datetime.now())

    # start the scheduler
    scheduler.start()

    try:
        while True:
            # simulate activity (which keeps the main thread alive)
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...")
        scheduler.shutdown()

if __name__=="__main__":
    main()

# json_body = [
#     {
#         "measurement": "cpu_load_short",
#         "tags": {
#             "host": "server01",
#             "region": "us-west"
#         },
#         "time": "2009-11-10T23:00:00Z",
#         "fields": {
#             "Float_value": 0.64,
#             "Int_value": 3,
#             "String_value": "Text",
#             "Bool_value": True
#         }
#     }
# ]