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
from api_daemon import db
from api_daemon import app
from api_daemon import Basic_url

#Query.remove_basic('www.dated1.pt')
#Query.remove_basic('www.dated2.pt')
#Query.remove_basic('www.dated3.pt')

#r = requests.get("http://services.web.ua.pt/parques/parques")
#print(r.json())

tokens = {}


# TRIM DOS ARGS NO BACKOFFICE!
"""
    args = val.args.split(',')
    for i in range(0,len(args)):
        args[i]=args[i].strip()
"""

def requests_basic(influx):
    print('STARTING BASIC\n')
    print(Query.get_basic_period(5))
    for val in Query.get_basic_period(5):
        # make request
        print('\n')
        print(val)
        print('\n')
        try:
            request_vals = make_request(val.url)
            # filter
            if val.args:
                args = val.args.split(',')
                try:
                    request_vals = filter_request(request_vals,args)
                except:
                    # set error e args = None
                    Query.change_basic(val.url,'error','FILTER FAILED')
                    Query.change_basic(val.url,'args','')
                    print("{val.url}: BASIC FILTER FAILED")
            #influx.write_points(request_vals, database="Metrics")  
            print('\n')
            print(val)
            print('\n')
            print(request_vals)
        except:
            print('{val.url}: BASIC FAILED')
            Query.pause_basic(val.url)
            Query.change_basic(val.url,'error','BAD REQUEST or AUTHENTICATION FAILED')
        
def requests_key(influx):       
    print('STARTING KEY\n')
    for val in Query.get_key_period(5): 
        # Make request
        try:
            request_vals = make_request_key(val.url,val.key)
            if val.args:
                args = val.args.split(',')
                # filter
                try:
                    request_vals = filter_request(request_vals,args)
                except:
                    Query.change_key(val.url,'error','FILTER FAILED')
                    Query.change_key(val.url,'args','')
                    print("{val.url}: KEY FILTER FAILED")
            #influx.write_points(request_vals, database="Metrics")  
            print(request_vals)
        except:
            print('{val.url}: KEY FAILED')
            Query.pause_key(val.url)
            Query.change_key(val.url,'error','BAD REQUEST or AUTHENTICATION FAILED')
        
def requests_http(influx):  
    print('STARTING HTTP\n')
    for val in Query.get_http_period(5):  
        try:
            request_vals = make_request_http(val.url,val.username,val.key)
            if val.args:
                args = val.args.split(',')
                try:
                    request_vals = filter_request(request_vals,args)
                except:
                    Query.change_http(val.url,'error','FILTER FAILED')
                    Query.change_http(val.url,'args','')
                    print("{val.url}: HTTP FILTER FAILED")
            #influx.write_points(request_vals, database="Metrics")  
            print(request_vals)
        except:
            print('{val.url}: HTTP FAILED')
            Query.pause_http(val.url)
            Query.change_http(val.url,'error','BAD REQUEST or AUTHENTICATION FAILED')
        
        
def requests_token(influx):
    print('STARTING TOKEN\n')
    print(Query.get_token_period(5))
    for val in Query.get_token_period(5):
        # ver se o token já foi pedido
        print('\n')
        print(val)
        print('\n')
        if not val.url in tokens:
            tokens[val.url] = ''
        try:
            check = 0
            # se o token não estiver disponivel make_request
            if not tokens[val.url]:
                tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
            while 1:
                r = make_request_token(val.url,tokens[val.url])
                # se der erro pedir token
                if r.status_code >= 400:
                    tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
                    # sair do loop se continuar a dar erro
                    print('TOKEN REQUESTING ...')
                    if check > 3:
                        Query.change_token(val.url,'error','TOKEN REQUEST FAILED')
                        Query.pause_token(val.url)
                        print("{val.url}: TOKEN REQUEST FAILED")
                        break
                if r.status_code<400:
                    # request succeeded
                    print('TOKEN REQUEST SUCCESS')
                    check=8
                    break
                check += 1
                
            # if request succeeded
            if check==8:
                request_vals = make_request_token(val.url,tokens[val.url])
                if val.args:
                    args = val.args.split(',')
                    for i in range(0,len(args)):
                        args[i]=args[i].strip()
                    try:
                        Query.change_token(val.url,'args','')
                        request_vals = filter_request(request_vals,args)
                    except:
                        Query.change_token(val.url,'error','FILTER FAILED')
                        print("{val.url}: TOKEN FILTER FAILED")
                #influx.write_points(request_vals, database="Metrics")     
                print('\n')
                print(val)
                print('\n')   
                print(request_vals)
            else:
                # remover do dict
                print('TOKEN REMOVED')
                del tokens[val.url]
        except:
            print('{val.url}: TOKEN FAILED')
            Query.pause_token(val.url)
            Query.change_token(val.url,'error','BAD REQUEST or AUTHENTICATION FAILED')

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
    influx = InfluxDBClient(host='127.0.0.1', port=8086, username="daemon", password="daemon_1234")
    # add jobs
    scheduler.add_job(requests_basic, trigger="interval", args=[influx], minutes=1, id="5minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(requests_key, trigger="interval", args=[influx], minutes=1, id="5minjob_key", next_run_time=datetime.now())
    scheduler.add_job(requests_http, trigger="interval", args=[influx], minutes=1, id="5minjob_http", next_run_time=datetime.now())
    scheduler.add_job(requests_token, trigger="interval", args=[influx], minutes=1, id="5minjob_token", next_run_time=datetime.now())
    # start the scheduler
    scheduler.start()
    try:
        while True:
            # simulate activity (which keeps the main thread alive)
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...\n")
        scheduler.remove_job('5minjob_basic')
        scheduler.remove_job('5minjob_key')
        scheduler.remove_job('5minjob_http')
        scheduler.remove_job('5minjob_token')
        scheduler.shutdown()

if __name__=="__main__":
    main()