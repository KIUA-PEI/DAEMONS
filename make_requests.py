import time
import threading

from datetime import datetime
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
from api_daemon import Query
from make_requests_utils import *

influx = InfluxDBClient(host='40.68.96.164', port=8086, username="peikpis", password="peikpis_2021")

def make_request(period):
    
    for val in Query.get_basic_period(period):
        request_basic(val[0])
        
    
    for val in Query.get_key_period(period): 
        request_key(val)
        
        
    for val in Query.get_http_period(period):
        request_http(val)
    
      
    for val in Query.get_token_period(period):
        request_token(val)
     

def start_requests_basic(period):
    threads = []

    for val in Query.get_basic_period(period):
        threading.Thread(target=request_basic(val[0]))
    
    for thread in threads:
        thread.join()

def start_requests_key(period):
    threads = []

    for val in Query.get_key_period(period):
        threading.Thread(target=request_key(val))
    
    for thread in threads:
        thread.join()

def start_requests_http(period):
    threads = []

    for val in Query.get_http_period(period):
        threading.Thread(target=request_http(val))
    
    for thread in threads:
        thread.join()

def start_requests_token(period):
    threads = []

    for val in Query.get_token_period(period):
        threading.Thread(target=request_token(val))
    
    for thread in threads:
        thread.join()


def main():
    """
    print('STARTING ...')
    print('_____________________________________________________')
    print('Basic\n')
    print(Query.get_basics())
    print('\n')
    print('_____________________________________________________')
    print('Key\n')
    print(Query.get_keys())
    print('\n')
    print('_____________________________________________________')
    print('Http\n')
    print(Query.get_https())
    print('\n')
    print('_____________________________________________________')
    print('Token\n')
    print(Query.get_tokens())
    print('\n')
    print('_____________________________________________________')
    print('\n')
    """
    # start scheduler
    scheduler = BackgroundScheduler()
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)
    
    scheduler.add_job(start_requests_basic, trigger="interval", args=[5], minutes=5, id="5minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[15], minutes=15, id="15minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[30], minutes=30, id="30minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[60], minutes=60, id="60minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[1440], minutes=1440, id="dailyjob_basic", next_run_time=datetime.now())

    scheduler.add_job(start_requests_key, trigger="interval", args=[5], minutes=5, id="5minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[15], minutes=15, id="15minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[30], minutes=30, id="30minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[60], minutes=60, id="60minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[1440], minutes=1440, id="dailyjob_key", next_run_time=datetime.now())

    scheduler.add_job(start_requests_http, trigger="interval", args=[5], minutes=5, id="5minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[15], minutes=15, id="15minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[30], minutes=30, id="30minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[60], minutes=60, id="60minjob_http", next_run_time=datetime.now()) 
    scheduler.add_job(start_requests_http, trigger="interval", args=[1440], minutes=1440, id="dailyjob_http", next_run_time=datetime.now())  

    scheduler.add_job(start_requests_token, trigger="interval", args=[5], minutes=5, id="5minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[15], minutes=15, id="15minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[30], minutes=30, id="30minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[60], minutes=60, id="60minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[1440], minutes=1440, id="dailyjob_token", next_run_time=datetime.now())

    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...\n")  
        scheduler.shutdown()
if __name__=="__main__":
    main()