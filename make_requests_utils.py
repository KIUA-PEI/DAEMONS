from api_daemon import Query
from utils import *
from make_requests import *

tokens = {}

# se calhar caso não tenha args usar merge_filter(vals,vals.keys) -> tudo
def format_influx(metric_id,data):
    result = []
    for entry in [entry for entry in data if entry]:
        add_entry = {"measurement":metric_id,"tags":{'id':metric_id}}
        #print(entry)
        if 'Timestamp' in entry:
            add_entry['time'] = str(entry['Timestamp'])
            del entry['Timestamp']
        else:
            add_entry['time'] = str(get_timestamp())
        

        #fields = []
        #for key in entry:
        #    fields.append({key:entry[key]})
        
        add_entry['fields'] = entry
        
        result.append(add_entry)
    
    return result 

def request_basic(url):
    print('STARTING BASIC\n')
    request = requests.get(url,timeout=25)
    if request.status_code == 200: 
        # val[0] -> args ,val[1] -> id 
        for val in Query.get_basic_args(url):
            args = [arg.strip() for arg in val[0].split(',')] if val[0] else 1
            try:
                db_entrys = format_influx(val[1],merge_filter(request.json(),args))
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Test")
                    except:
                        print('influx failed')
                else:
                    print('BAD FORMAT')
            except:
                Query.pause_basic(val[1])
                print("FILTER FAILED")        
            
    elif request.status_code == 401:
        Query.pause_basic_url(val[1])
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_basic_url(val[1])
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_basic_url(val[1])
        print('URL NOT FOUND')
    else:
        print('bad request')
        Query.pause_basic_url(val[1])
    return False

def request_key(val):       
    print('STARTING KEY\n')
    
    request = requests.get(val.url,headers={'Authorization': val.key},timeout=25)
    if request.status_code < 400:
            args = [arg.strip() for arg in val.args.split(',')] if val.args else request.json().keys()
            print('key',val.url,args)
            try:
                db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args))
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Test")
                    except:
                        print('influx failed')
                else:
                    print('BAD FORMAT')
            except:
                Query.pause_key(val.metric_id)
                print("FILTER FAILED")
                return False
    elif request.status_code == 401:
        Query.pause_key(val.metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_key(val.metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_key(val.metric_id)
        print('URL NOT FOUND')
    else:
        print('bad request')
        Query.pause_key(val.metric_id)
        
    return False

def request_http(val):  
    print('STARTING HTTP\n')
    request = requests.get(val.url,headers={"userName": val.username , "password": val.key},timeout=25)
    if request.status_code < 400:    
        if val.args:
            args = [arg.strip() for arg in val.args.split(',')]
            print('http',val.url,args)
            try:
                db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args))
                # enviar para a influx
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Test")
                    except:
                        print('influx failed')
                else:
                    print('BAD FORMAT')
            except:
                Query.pause_http(val.metric_id)
                print("FILTER FAILED")     
        else:
            print('SEND TO INFLUX')   
    elif request.status_code == 401:
        Query.pause_http(val.metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_http(val.metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_http(val.metric_id)
        print('URL NOT FOUND')
    else:
        print('bad request')
        Query.pause_http(val.metric_id)
        
    return False
        
def request_token(val):
    print('STARTING TOKEN\n')
    check = 0
    
    if not val.url in tokens:
        tokens[val.url] = None
        while not tokens[val.url]:
            tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
            if check >= 4:
                print('token request failed')
                Query.pause_token(val.metric_id)
                return False
    
    check = 0
   
    while check < 4:
        request = requests.get(val.url,headers={'Authorization': tokens[val.url]},timeout=25)
        if request.status_code<=200:
            args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
            try:
                db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args+['first']))
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Test")
                    except:
                        print('influx failed')
                else:
                    print('BAD FORMAT')
            except:
                Query.pause_token(val.metric_id)
                print("FILTER FAILED") 
                return False
            return
        elif request.status_code == 401:
            Query.pause_token(val.metric_id)
            print('Authentication Error')
        elif request.status_code == 403:
            Query.pause_token(val.metric_id)
            print("URL FORBIDEN OPERATION")
        elif request.status_code == 404:
            Query.pause_token(val.metric_id)
            print('URL NOT FOUND')
        elif request.status_code < 500:
            print('bad request')
            Query.pause_token(val.metric_id)
        else:
            check += 1
        
    return False
