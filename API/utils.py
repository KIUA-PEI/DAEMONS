# ficheiro com utils como make request
# get token
# make request_key
# make request_open
import requests
import json
import base64
import pytz
from pytz import timezone, common_timezones
from datetime import datetime

def make_request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return display_error(r.status_code)

def make_request_key(url,key):
    r = requests.get(url,headers={'Authorization': key})
    if r.status_code == 200:       
        return r.json()
    return display_error(r.status_code) 
        
def make_request_token(url,token):
    r = requests.get(url,headers={'Authorization': token})
    if r.status_code == 200:
        return r.json()
    return display_error(r.status_code)

# para o wso2 content_type -> application/x-www-form-urlencoded | auth_type -> Bearer
def get_token(url,key,secret,content_type=None,auth_type=None):
    msg = encode_b64(key+secret)
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg})
    if request_token.status_code >= 200:
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    return display_error(request_token.status_code)


def display_error(request_status):
    if request_status == 400:
        return "Bad Request"
    elif request_status == 404:
        return "Not Found"
    elif request_status == 401:
        return "Authentication Error"
    return "Unexpected Error"

def encode_b64(msg):
    msg_bytes = msg.encode('ascii')
    base = base64.b64encode(msg_bytes)
    return base.decode('ascii')

def get_timestamp():
    portugal_tz = timezone("Europe/Lisbon")
    return portugal_tz.localize(datetime.now())

def epoch2utc(timestamp):
    return datetime.fromtimestamp(timestamp, pytz.utc)

def create_entry(measurement, tags, timestamp, fields):
    """
    creates a json like influx db entry
    """
    return [{"measurement": measurement, "tags" : tags, "time" : timestamp, "fields": fields}]