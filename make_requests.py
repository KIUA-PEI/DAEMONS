#from DAEMONS.Api.utils import make_request
import time
import json
import requests

from datetime import datetime
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
from utils import *
from sqlalchemy import create_engine
from api_daemon import Query

from make_requests_utils import *

#Query.remove_basic('www.dated1.pt')
#Query.remove_basic('www.dated2.pt')
#Query.remove_basic('www.dated3.pt')

#r = requests.get("http://services.web.ua.pt/parques/parques")
#print(r.json())


# TRIM DOS ARGS NO BACKOFFICE!
"""
    args = val.args.split(',')
    for i in range(0,len(args)):
        args[i]=args[i].strip()
"""

def make_request(influx,period):
    for val in Query.get_basic_period(period):
        request_vals = request_basic(val)
        print(request_vals)
        print(period)
        try:
            influx.write_points(request_vals, database="Metrics")       
        except:
            print('INFLUX DOWN') 
    
    for val in Query.get_key_period(period): 
        request_vals = request_key(val)
        print(request_vals)
        try:
            influx.write_points(request_vals, database="Metrics")       
        except:
            print('INFLUX DOWN') 

    for val in Query.get_http_period(period):
        request_vals = request_http(val)
        print(request_vals)
        try:
            influx.write_points(request_vals, database="Metrics")       
        except:
            print('INFLUX DOWN') 
    
    for val in Query.get_token_period(period):
        print(val)
        request_vals = request_token(val)
        print(request_vals)
        try:
            influx.write_points(request_vals, database="Metrics")       
        except:
            print('INFLUX DOWN') 
    

def main():
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
    # start scheduler
    scheduler = BackgroundScheduler()
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)
    
    # start influxDBClient
    #try:
        #influx = InfluxDBClient(host='127.0.0.1', port=8086, username="daemon", password="daemon_1234")
        # add jobs
    if True:    
        influx = None
        scheduler.add_job(make_request, trigger="interval", args=[influx,5], minutes=5, id="5minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[influx,15], minutes=15, id="15minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[influx,30], minutes=30, id="30minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[influx,60], minutes=60, id="60minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[influx,1440], minutes=1440, id="dailyjob_basic", next_run_time=datetime.now())
        
        # start the scheduler
        scheduler.start()
        try:
            while True:
                # simulate activity (which keeps the main thread alive)
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            print("\nexiting...\n")
            scheduler.remove_job('15minjob_basic')
            scheduler.remove_job('15minjob_key')
            scheduler.remove_job('15minjob_http')
            scheduler.remove_job('15minjob_token')
            scheduler.shutdown()
            scheduler.shutdown()
    #except:
    #    print('Influx CLIENT ERROR')
if __name__=="__main__":
    main()