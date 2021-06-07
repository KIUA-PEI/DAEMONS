from api_daemon import Query
from utils import *
from make_requests import *

tokens = {}

# se calhar caso não tenha args usar merge_filter(vals,vals.keys) -> tudo

def request_basic(url):
    print('STARTING BASIC\n')
    request = requests.get(url,timeout=25)
    if request.status_code == 200: 
        # val[0] -> args ,val[1] -> id 
        print(request.json())
        print('query_args',Query.get_basic_args(url))
        print(len(Query.get_basic_args(url)))
        for val in Query.get_basic_args(url):
            print('basic',url,val)
            args = [arg.strip() for arg in val[0].split(',')] if val[0] else 1
            print('args',args)
            
            if True:
                db_entrys = merge_filter(request.json(),args)
                    #print('DONE',db_entrys)
                if 'Timestamp' in request.json():
                    print('Insert Time Stamp')
                for entry in db_entrys:
                    print(entry,url)
                # enviar para a influx
            #except:
            #    Query.pause_basic(val[1])
            #    print("FILTER FAILED")        

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
                db_entrys = merge_filter(request.json(),args)
                for entry in db_entrys:
                    print(entry,val.url)
                # enviar para a influx
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
                db_entrys = merge_filter(request.json(),args)
                # enviar para a influx
                for entry in db_entrys:
                    print(entry,val.url)
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
            if val.args:
                args = [arg.strip() for arg in val.args.split(',')]
                print(args)
                try:
                    db_entrys = merge_filter(request.json(),args)
                    # enviar para a influx
                    #print(db_entrys)
                    for entry in db_entrys:
                        print(entry)
                    return db_entrys
                except:
                    Query.pause_token(val.metric_id)
                    print("FILTER FAILED") 
                    return False
            else:
                print('SEND TO INFLUX')
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
        
        
    # enviar na função send to merge_filter ... e fazer erros na merge_filter tmb
    """
    if request.status_code <= 200:      
        if val.args:
            args = [arg.strip() for arg in val.args.split(',')]
            try:
                merge_filter(request.json(),args)
            except:
                Query.pause_token(val.metric_id)
                print("FILTER FAILED") 
        else:
            print('SEND TO INFLUX')
    else:
        Query.pause_token(val.metric_id)
    """
    return False
