#from DAEMONS.Api.utils import make_request
import requests
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

print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print(Basic_url.query.filter(Basic_url.status==True,Basic_url.period=='5').all())
print(Query.get_basics())
for val in Query.get_basic_period(5):
    print(val)
    print('\n')
    request_vals = make_request(val['url'])
    #result = filter_request(request_vals,val['args'])
    #print(result)

#for val in Query.get_basic_period(15): 
    
    
    
#for val in Query.get_basic_period(30):  
    
    

#for val in Query.get_basic_period(60):