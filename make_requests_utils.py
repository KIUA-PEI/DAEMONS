from api_daemon import Query
from utils import *

tokens = {}

def request_basic(val):
    print('STARTING BASIC\n')
    request = requests.get(val.url)
    
    if request.status_code < 400:
        if val.args:
            args = val.args.split(',')
            try:
                request_vals = filter_request(request.json(),args)
                if not request_vals:
                    print("FILTER FAILED")
                    Query.pause_basic(val.url)
                    Query.change_basic(val.url,'error','BAD FILTER (no fields found)')
                    return False
                return request_vals
            except:
                Query.pause_basic(val.url)
                Query.change_basic(val.url,'error','BAD FORMAT')
                print("FILTER FAILED")
                return False
            
    Query.pause_basic(val.url)
    Query.change_basic(val.url,'error',display_error(request.status_code))
    return False 


def request_key(val):       
    print('STARTING KEY\n')
    
    request = requests.get(val.url,headers={'Authorization': val.key})
    if request.status_code < 400:
        if val.args:
            args = val.args.split(',')
            # filter
            try:
                request_vals = filter_request(request.json(),args)
                if not request_vals:
                    Query.pause_key(val.url)
                    Query.change_key(val.url,'error','BAD FILTER (no fields found)')
                    print("FILTER FAILED")
                    return False
                return request_vals
            except:
                Query.pause_key(val.url)
                Query.change_key(val.url,'error','BAD FORMAT')
                print("FILTER FAILED")
                
    Query.pause_key(val.url)
    Query.change_key(val.url,'error',display_error(r.status_code))
    return False 


def request_http(val):  
    print('STARTING HTTP\n')
    request = requests.get(val.url,headers={"userName": val.user , "password": val.key})
    if request.status_code < 400:    
        if val.args:
            args = val.args.split(',')
            try:
                request_vals = filter_request(request_vals,args)
                if not request_vals:
                    Query.pause_http(val.url)
                    Query.change_http(val.url,'error','BAD FILTER (no fields found)')
                    print("FILTER FAILED")
                    return False 
                return request_vals    
            except:
                Query.change_http(val.url,'error','BAD FORMAT')
                Query.change_http(val.url,'args','')
                print("FILTER FAILED")        
    Query.pause_http(val.url)
    Query.change_http(val.url,'error',display_error(request.status_code))
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
        request = requests.get(val.url,headers={'Authorization': tokens[val.url]})
        # se der erro pedir token
        if request.status_code == 403:
            tokens[val.url] = get_token(val.token_url,val.key,val.secret,val.content_type,val.auth_type)
            # sair do loop se continuar a dar erro
            if check > 3:
                Query.change_token(val.url,'error','TOKEN REQUEST FAILED')
                Query.pause_token(val.url)
                print("TOKEN REQUEST FAILED")
                break
        if request.status_code<=200:
            check = -1
            break
        check += 1
                
    if request.status_code <= 200:
            
        if val.args:
            args = val.args.split(',')
            for i in range(0,len(args)):
                args[i]=args[i].strip()
            try:
                request_vals = filter_request(request.json(),args)
                if not request_vals:
                    Query.pause_token(val.url)
                    Query.change_token(val.url,'error','BAD FILTER (no fields found)')
                    print("FILTER FAILED")
                    return False 
                return request_vals
            except:
                Query.pause_token(val.url)
                Query.change_token(val.url,'error','BAD FORMAT')
                print("FILTER FAILED") 
    else:
        Query.pause_token(val.url)
        Query.change_token(val.url,'error',display_error(request.status_code))

    
    return False
        
        