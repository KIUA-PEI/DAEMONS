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
        
def make_request_http(url,user,key):
    pass
        
def make_request_token(url,token):
    print('REQUESTING')
    r = requests.get(url,headers={'Authorization': token})
    if r.status_code == 200:
        print('NICE')
        return r.json()
    print('NOT NICE')
    return display_error(r.status_code)

# para o wso2 content_type -> application/x-www-form-urlencoded | auth_type -> Bearer
def get_token(url,key,secret,content_type=None,auth_type=None):
    msg = encode_b64(key+':'+secret)
    #print(msg=='al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h')
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg})
    if request_token.status_code < 400:
        print('Token OK!')
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    print('BAD TOKEN')
    print(request_token)
    return display_error(request_token.status_code)

def send_influx():
    pass

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
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

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

# só pode receber certos tipos de dados ...
def filter_request(vals,args):
      
    for field in [field for field in vals if field not in args]:
        if isinstance(field,str):
            if isinstance(vals[field],list) or isinstance(vals[field],set):
                i=0
                for v in vals[field]:
                    vals[field][i] = filter_request(v,args)  
                    i+=1
                continue
            if isinstance(vals[field],dict):
                for key in vals[field].keys():
                    if not key in args:
                        del vals[key]
                continue
            if not field in args:
                del vals[field]
            continue  
        if isinstance(field,dict):
            filter_request(field,args)
            continue 
        if isinstance(field,list):
            for v in field:
                filter_request(v,args) 
            continue
        return 'UNKNOWN FORMAT'
    for val in vals:
        if not val:
            vals.remove(val)
    return vals

def filter_request_add(vals,args):
    result = {}
    
    for field in vals.keys():
        if isinstance(vals[field],list) or isinstance(vals[field],set):
            for v in vals[field]:
                aux = filter_request(v,args)
                for key in aux:
                    if key in result:
                        result[key] += aux[key]
                    else:
                        result[key] = aux[key]   
            continue
        if field in args:
            print(vals[field])
            result[field] = vals[field]
    return result

# test filter_request

#args = {"accessPoints"}
# depois testar 
#args = {"accessPoints": ["clientCount","macAddress","location"]}

args = ["first","count","clientCount","macAddress","location"]

url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='
token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
auth_type = 'Bearer'
content_type = 'application/x-www-form-urlencoded'
key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'
# get_token(url,key,secret,content_type=None,auth_type=None)
token = get_token(token_url,key,secret,content_type,auth_type)
for i in range(8):
    r = make_request_token(url+str(i*100),token)
    print('YES\n')
    #print(r['accessPoints'][0]['macAddress'])
    data = filter_request(r,args)
    print(data)
    #print('\n')
    #print(data['accessPoints'][0])
    #print('\n')
    #print(data["accessPoints"])
    #print('\n') 

