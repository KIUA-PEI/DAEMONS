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


#clientCount by location ... tem que estar tudo no mesmo field
def merge_entrys2(entrys,data):
    for row in [row for row in data]:
        for entry in entrys:
            for key in [key for key in entry if not key in row]:
                row[key] = entry[key]
            for key in [key for key in row if not key in entry]:
                entry[key] = row[key]
            data.append(entry)
    print('finaly')
    return data

def merge_entrys(entrys,data):

    for row in [row for row in entrys if row.keys() == data[0].keys()]:
        data.append(row)
        entrys.remove(row)
        
    merge_data = {}
    for key in data[0]:
        merge_data[key] = data[0][key]
    
    for entry in entrys:
        entry.update(merge_data)
        data.append(entry)
    
    return data

def merge_fields(field,data):
    for row in field:
        for val in data:
            val.update(row)
    
    return data
    

def merge_filter(data,args):
    entrys = []
    for field in [field for field in data]:
        if isinstance(field,str):          
            
            if isinstance(data[field],dict):
                if entrys:
                    entrys+=merge_entrys(merge_filter(data[field],args),entrys)
                else:
                    entrys=merge_entrys(merge_filter(data[field],args),entrys)
            elif not isinstance(data[field],str) and isinstance(data[field],list): 
                aux = []
                for val in data[field]:
                    aux += merge_entrys((merge_filter(val,args)),entrys) if entrys else merge_filter(val,args)
                entrys = aux
            elif args == 1:
                if entrys:
                    entrys=merge_fields([{field:data[field]}],entrys)
                else:
                    entrys.append({field:data[field]})
            elif field in args:
                if entrys:
                    entrys=merge_fields([{field:data[field]}],entrys)
                else:
                    entrys.append({field:data[field]})
        
        elif isinstance(field,dict):
            if entrys:
                entrys = merge_entrys((merge_filter(field,args)),entrys) if entrys else merge_filter(field,args)
            else:
                entrys = merge_filter(field,args)
        
        elif isinstance(field,list):
            aux = []
            for val in field:
                aux += merge_entrys((merge_filter(val,args)),entrys) if entrys else merge_filter(val,args)
            entrys = aux
    
    return entrys
