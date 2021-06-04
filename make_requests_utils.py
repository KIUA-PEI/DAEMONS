from api_daemon import Query
from utils import *
from make_requests import *

tokens = {}

def request_basic(url):
    print('STARTING BASIC\n')
    print(url)
    request = requests.get(url,timeout=25)
    if request.status_code < 400: 
        # val[0] -> args ,val[1] -> id 
        for val in Query.get_basic_args(url):
            if val[0]:
                args = [arg.strip() for arg in val[0].split(',')]
                try:
                    send_influx(request.json(),args)
                except:
                    Query.pause_basic(val[1])
                    Query.change_basic(val[1],'error','BAD FORMAT')
                    print("FILTER FAILED")
                    return False
            else:  
                print('Send 2 influx')
    else:
        Query.pause_basic_url(url)
    return False

def request_key(val):       
    print('STARTING KEY\n')
    
    request = requests.get(val.url,headers={'Authorization': val.key},timeout=25)
    if request.status_code < 400:
        if val.args:
            args = [arg.strip() for arg in val.args.split(',')]
            # filter
            try:
                send_influx(request.json(),args)
            except:
                Query.pause_key(val.metric_id)
                print("FILTER FAILED")
        else:
            print('SEND TO INFLUX')       
    else:
        Query.pause_key(val.metric_id)
    return False

def request_http(val):  
    print('STARTING HTTP\n')
    request = requests.get(val.url,headers={"userName": val.username , "password": val.key},timeout=25)
    if request.status_code < 400:    
        if val.args:
            args = [arg.strip() for arg in val.args.split(',')]
            try:
                send_influx(request.json(),args)
            except:
                Query.pause_http(val.metric_id)
                print("FILTER FAILED")     
        else:
            print('SEND TO INFLUX')   
    else:
        Query.pause_http(val.metric_id)
    return False
        
def request_token(val):
    print('STARTING TOKEN\n')
    if not val.url in tokens:
        tokens[val.url] = ''
    check = 0
    # se o token não estiver disponivel make_request
    if not tokens[val.url]:
        tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
    while 1:
        request = requests.get(val.url,headers={'Authorization': tokens[val.url]},timeout=25)
        # se der erro pedir token
        if request.status_code >= 400:
            tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
            # sair do loop se continuar a dar erro
            if check > 3:
                Query.pause_token(val.metric_id)
                print("TOKEN REQUEST FAILED")
                break
            check += 1
        if request.status_code<=200:
            break
        
    # enviar na função send to send_influx ... e fazer erros na send_influx tmb
    if request.status_code <= 200:      
        if val.args:
            args = [arg.strip() for arg in val.args.split(',')]
            try:
                send_influx(request.json(),args)
            except:
                Query.pause_token(val.metric_id)
                print("FILTER FAILED") 
        else:
            print('SEND TO INFLUX')
    else:
        Query.pause_token(val.metric_id)
    return False
