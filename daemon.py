import requests
import time
import json
import kafka

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from kafka import KafkaProducer
from metrics import parking_data, get_acess_token, data_wirelessUsers
from consts import *

# jobs
def hour_job():
    print("this job runs every 1 hour")

def ten_sec_job(producer):
    i = 0
    while True:
        data = {"park":i}
        i = i + 1
        producer.send("parking", value=data)
        print("sended" + str(data))
        time.sleep(5)

def thirty_sec_job():
    print("this job runs every 30 sec")

def twenty_min_job(producer, token, keys):
    # parking data
    parking = parking_data()
    keys["parking"] = keys["parking"] + 1
    producer.send("parking", value={"PARK"+str(keys["parking"]) : parking})

    # number of wireless users data
    wireless_users = data_wirelessUsers(token)
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
    parkkey = 0

    # get primecoreAPI access token
    token = get_acess_token()

    # add jobs
    scheduler.add_job(hour_job, trigger="interval", hours=1, id="1hourjob")
    scheduler.add_job(ten_sec_job, trigger="interval", args=[producer], seconds=10, id="10secjob")
    scheduler.add_job(thirty_sec_job, trigger="interval", seconds=30, id="30secjob")
    scheduler.add_job(twenty_min_job, trigger="interval", args=[producer, token, KAFKAKEYS], minutes=20, id="20minjob", next_run_time=datetime.now())

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