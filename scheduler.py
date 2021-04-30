#   tentar automatizar o daemon
#   ter um url como arg
#   dar como argumento o token com opção de null
#   dar launch a esse daemon e 
#   enviar a informação para a database e katka
#   permitir ter uma lista de (url,key)'s para dar launch


import requests
import time
import json
import kafka

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from kafka import KafkaProducer

producer = ""
parkkey = 1

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

def twenty_min_job(url,producer, parkkey):
    r = requests.get(url)
    parking = r.json()
    timestamp = parking.pop(0)
    parking = [{"Nome":park["Nome"], "Capacidade" : park["Capacidade"], "Ocupado" : park["Ocupado"], "Livre" : park["Livre"]} for park in parking]
    parking.insert(0, timestamp)
    producer.send("parking", value={"PARK"+str(parkkey) : parking})
    parkkey = parkkey + 1
    print("sended" + str({"PARK"+str(parkkey) : parking}))


def launch_daemon(url,key=None):
    print("runs main")
    # start scheduler
    scheduler = BackgroundScheduler()
    
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    # cuidado com a timezone
    scheduler.configure(job_defaults=job_defaults)

    # start Kafka Python Client
    producer = KafkaProducer(bootstrap_servers=['13.69.49.187:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    parkkey = 0

    # add jobs
    scheduler.add_job(hour_job, trigger="interval", hours=1, id="1hourjob")
    scheduler.add_job(ten_sec_job, trigger="interval", args=[producer], seconds=10, id="10secjob")
    scheduler.add_job(thirty_sec_job, trigger="interval", seconds=30, id="30secjob")
    scheduler.add_job(twenty_min_job, trigger="interval", args=[url,producer, parkkey], minutes=20, id="20minjob", next_run_time=datetime.now())

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
    launch_daemon("http://services.web.ua.pt/parques/parques")