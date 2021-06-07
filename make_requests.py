#from DAEMONS.Api.utils import make_request
import time
#import json
#import requests

from datetime import datetime
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
#from sqlalchemy import create_engine
from api_daemon import Query
from make_requests_utils import *
#import signal


#from functools import wraps
#import errno
#import os
#import signal
"""
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
"""
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

influx = None
#try:
    #influx = InfluxDBClient(host='127.0.0.1', port=8086, username="daemon", password="daemon_1234")
#except:
#   print('influx down')
#class TimeoutException(Exception):   # Custom exception class
#    pass

#def timeout_handler(signum, frame):   # Custom signal handler
#    raise TimeoutException

#signal.signal(signal.SIGALRM, timeout_handler)



def make_request(period):
    # distinct URL's ... pode ter repetidos
    """
    x=0
    signal.alarm(15) 
    try:         
        while 1:
            x+=1 
    except TimeoutException:
            print('TIME EXCEPTION')  
    finally:
        signal.alarm(0)
    print(x)
    """ 
    for val in Query.get_basic_period(period):
        print('basic')
        print(val[0])
        print('\n')
        request_basic(val[0])
        
    
    for val in Query.get_key_period(period): 
        print('key')
        print(val)
        print('\n')
        request_key(val)
        
        
    for val in Query.get_http_period(period):
        print('http')
        print(val)
        print('\n')
        request_http(val)
        
      
    for val in Query.get_token_period(period):
        print('token')
        print(val)
        print('\n')
        request_token(val)
    

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
        scheduler.add_job(make_request, trigger="interval", args=[5], minutes=5, id="5minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[15], minutes=15, id="15minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[30], minutes=30, id="30minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[60], minutes=60, id="60minjob_basic", next_run_time=datetime.now())
        
        scheduler.add_job(make_request, trigger="interval", args=[1440], minutes=1440, id="dailyjob_basic", next_run_time=datetime.now())
        
        # start the scheduler
        scheduler.start()
        try:
            while True:
                # simulate activity (which keeps the main thread alive)
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            print("\nexiting...\n")
            scheduler.remove_job('5minjob_basic')
            scheduler.remove_job('15minjob_basic')
            scheduler.remove_job('30minjob_basic')
            scheduler.remove_job('dailyjob_basic')
            scheduler.shutdown()
            scheduler.shutdown()
    #except:
    #    print('Influx CLIENT ERROR')
if __name__=="__main__":
    main()