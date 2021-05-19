#from DAEMONS.Api.utils import make_request
import time
import json
import requests

from datetime import datetime
#from influxdb import InfluxDBClient
#from apscheduler.schedulers.background import BackgroundScheduler
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

print(Basic_url.query.filter(Basic_url.status==True,Basic_url.period=='5').all())
print('\n')
print(Query.get_basics())
print('\n')

for val in Query.get_basic_period(5):
    print(val.url)
    print(val.args)
    
    print(val.args)
    try:
        request_vals = make_request(val.url)
        if val.args:
            args = val.args.split(',')
            for i in range(0,len(args)):
                args[i]=args[i].strip()
            try:
                request_vals = filter_request(request_vals,args)
            except:
                print("FILTER FAILED")
        print(request_vals)
    except:
        print('FAILED')
        Query.pause_basic(val.url)
        print(Query.get_basic_period(5))
        Query.start_basic(val.url)
        print(Query.get_basic_period(5))
    #request_vals = filter_request(request_vals,args)
    
    
for val in Query.get_basic_period(15): 
    print(val.url)
    try:
        request_vals = make_request(val.url)
        if val.args:
            args = val.args.split(',').strip()
            try:
                request_vals = filter_request(request_vals,args)
            except:
                print("FILTER FAILED")
        print(request_vals)
    except:
        print('FAILED')
        Query.pause_basic(val.url)
    
    
for val in Query.get_basic_period(30):  
    print(val.url)
    try:
        request_vals = make_request(val.url)
        if val.args:
            args = val.args.split(',').strip()
            try:
                request_vals = filter_request(request_vals,args)
            except:
                print("FILTER FAILED")
        print(request_vals)
    except:
        print('FAILED')
        Query.pause_basic(val.url)
    

for val in Query.get_basic_period(60):
    print(val.url)
    try:
        request_vals = make_request(val.url)
        if val.args:
            args = val.args.split(',').strip()
            try:
                request_vals = filter_request(request_vals,args)
            except:
                print("FILTER FAILED")
        print(request_vals)
    except:
        print('FAILED')
        Query.pause_basic(val.url)