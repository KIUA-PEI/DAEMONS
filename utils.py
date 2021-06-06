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
from make_requests import influx



def make_request(url):  
    r = requests.get(url,timeout=15)
    if r.status_code == 200:
        return r.json()
    return display_error(r.status_code)
        

def make_request_key(url,key):
    return requests.get(url,headers={'Authorization': key},timeout=15)
   
def make_request_http(url,user,key):
    return requests.get(url,headers={"userName": user , "password": key},timeout=15)

def make_request_token(url,token):
    return requests.get(url,headers={'Authorization': token},timeout=15)
    

# para o wso2 content_type -> application/x-www-form-urlencoded | auth_type -> Bearer
def get_token(url,key,secret,content_type=None,auth_type=None):
    msg = encode_b64(key+':'+secret)
    #print(msg=='al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h')
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
    if request_token.status_code < 400:
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    return False
    
def send_influx():
    pass

def display_error(request_status):
    if request_status == 404:
        return "URL Not Found"
    elif request_status == 401:
        return "Authentication Error"
    elif request_status == 403:
        return "URL FORBIDEN OPERATION"
    return "Bad Request"

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
    if not isinstance(vals, str):
        for field in [field for field in vals]:
            if isinstance(field,str):
                if (isinstance(vals[field],list) or isinstance(vals[field],set)):
                    i=0
                    for v in vals[field]:
                        vals[field][i] = filter_request(v,args)  
                        i+=1
                    continue
                if isinstance(vals[field],dict):
                    aux = list(vals[field].keys())
                    for key in aux:
                        if not key in args:
                            del vals[field][key]
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
            return []
        for val in vals:
            if not val:
                vals.remove(val)
    return vals
#clientCount by location ... tem que estar tudo no mesmo field
def merge_entrys(entry,data):
    
    for val in [val for val in data]:
        if isinstance(entry,dict):
            for key in entry:
                if not isinstance(entry[key],str) and isinstance(entry[key],list):
                    for v in entry[key]:
                        val[key] = v
                else:    
                    val[key] = entry[key]
        if isinstance(entry,list):
            aux = val
            data.remove(val)
            for row in entry:
                if isinstance(row,dict):
                    aux.update(aux)
                    data.append(row)
            
    return data

def merge_filter(data,args):
    entrys = []
    for field in [field for field in data]:   
        if isinstance(field,str):          
            if isinstance(data[field],dict):
                entrys=merge_entrys(merge_filter(data[field],args),entrys)
            elif not isinstance(data[field],str) and isinstance(data[field],list): 
                aux = []
                for val in data[field]:
                    print('val',val)
                    aux+=merge_entrys((merge_filter(val,args)),entrys)
                for val in aux:
                    print('aux_val',val)
                entrys = aux
            elif field in args:
                if entrys:
                    entrys=merge_entrys({field:data[field]},entrys)
                else:
                    entrys.append({field:data[field]})
        elif isinstance(field,dict):
            for val in merge_filter(field,args):
                entrys.append(val)
        elif isinstance(field,list):
            for aux in field:
                for val in merge_filter(aux,args):
                    entrys.append(val)
    
    return entrys

def send_influx(data,args):
    for field in [field for field in data]:    
        if isinstance(field,str):
            if field == args[0]:
                result = [{"measurment":"table_name","Timestamp" : str(get_timestamp())}, data[field]]
                for val in data:
                    if val in args[1:]:
                        print(field)
                        result.append(data[val])
                print('SEND TO INFLUX: ')
                print(result)  
                if influx:
                    try:
                        #[{"measurement": measurement, "tags" : tags, "time" : timestamp, "fields": fields}]
                        influx.write_points(json.dumps(result), database="Metrics")       
                    except:
                        print('INFLUX DOWN')    
                pass
            elif isinstance(data[field],dict):
                send_influx(data[field],args)    
            elif not isinstance(data[field],str) and isinstance(data[field],list):
                send_influx(data[field],args)    
        if isinstance(field,dict):
            send_influx(field,args)
        if isinstance(field,list):
            send_influx(field,args)
                 
            
# gramatica ... clientCount, location and macAddress
# 
"""
args = ["clientCount","location","macAddress"]
url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?maxResult=1000&firstResult='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?id='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/Building'
token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
auth_type = 'Bearer'
content_type = 'application/x-www-form-urlencoded'
key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'
# get_token(url,key,secret,content_type=None,auth_type=None)
token = get_token(token_url,key,secret,content_type,auth_type)
for i in range(8):
    r = make_request_token(url+(str(i*10)),token)
    print(r)
    print(r.json())
    send_influx(r.json(),args)
"""
