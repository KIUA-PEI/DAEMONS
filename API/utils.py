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
    msg = encode_b64(key+':'+secret)
    print(msg=='al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h')
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg})
    if request_token.status_code < 400:
        print('Token OK!')
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    print('BAD TOKEN')
    print(request_token)
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

# args -> ficheiro json da db do url 
# vals -> ficheiro json que recebeu da API
def filter_request(vals,args):
    result = {}
    # converter args em dict
    # converter vals em dict
    
    for field in args:
        # USAR TRY CATCH !!! se der erro mudar o status do url para invalido ou os args = None
        #print(field)
        #print(args[field])
        if isinstance(args[field],list) or isinstance(args[field],set):
            # vai buscar todos os valores da lista arg
            result[field] = []
            for val in args[field]:
                #print('\n')
                #print(field)
                #print(result)
                #print(val)
                #print(vals[field])
                #print('\n')
                if isinstance(vals[field],list):
                    #print('ASDASDASDASD')
                    #print(result)
                    #print('\n')
                    for v in vals[field]:
                        result[field].append(v[val])
                    continue 
                if isinstance(vals[field],dict):
                    result[field].append(v[val])
            continue       
        result[field] = vals[field]
    return result


# test filter_request

#args = {"accessPoints"}
# depois testar 
args = {"accessPoints": ["name","macAddress","location"]}
url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='
token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
auth_type = 'Bearer'
content_type = 'application/x-www-form-urlencoded'
key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'
# get_token(url,key,secret,content_type=None,auth_type=None)
token = get_token(token_url,key,secret,content_type,auth_type)
for i in range(2):
    r = make_request_token(url+str(i*100),token)
    print(r)
    v = filter_request(r,args)
    #print(v)
    print('\n')
    print('\n')
    print('\n')
    print('\n')

# CRIAR UMA MANEIRA DE PROCURAR UMA CERTA KEY EM todo o DICT
# tipo args = first,count,last,macAddress
# vai buscar todos os valores do dicionario em que a key é uma dessas ...
# e fica +- result = {"first":v1,"last":v2,}
# TENTAR VER SE O SWAGGER NO PYTHON SERVE PARA IR BUSCAR CERTOS VALORES 

# ...
# if not isinstance(list) adicionar ao result
# if isinstance(list) ver key a key
# [accessPoints,macAddress,...]
# vals[accessPoints][macAddress][...]