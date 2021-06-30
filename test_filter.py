import requests
import base64
def encode_b64(msg):
    msg_bytes = msg.encode('ascii')
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

def get_token(url,key,secret,content_type=None,auth_type=None):
    msg = encode_b64(key+':'+secret)
    #print(msg=='al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h')
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
    if request_token.status_code < 400:
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    return False

def merge_entrys(entrys,data):
    # vai adicionar o elemento de uma lista com as mesmas keys
    for row in [row for row in entrys if row.keys() == data[0].keys()]:
        data.append(row)
        entrys.remove(row)
        
    # vai ver as keys que não estão na data    
    # como supostamente as keys na data são iguais para todos os membros só é preciso ver o primeiro
    merge_data = {}
    for key in [key for key in data[0] if not key in entrys[0]]:
        merge_data[key] = data[0][key]
    
    # adicionar as keys ás novas entradas
    for entry in entrys:
        entry.update(merge_data)
        data.append(entry)
        
    # é preciso limpar os elementos de data ... 
    # caso as keys sejam diferentes pode adicionar as keys de data a entrys 
    # mas algumas entradas de data ficam sem as keys de entrys
    # é preciso remover esses casos ...
    if entrys:
        for entry in data:
            if len(entry.keys()) < len(entrys[0].keys()):
                data.remove(entry)
        
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
                    entrys=merge_entrys(merge_filter(data[field],args),entrys)
                else:
                    entrys=merge_entrys(merge_filter(data[field],args),entrys)
            elif not isinstance(data[field],str) and isinstance(data[field],list): 
                aux = []
                for val in data[field]:
                    aux += merge_filter(val,args)
                entrys = merge_entrys(aux,entrys) if entrys else aux
                
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
                entrys = merge_entrys((merge_filter(field,args)),entrys)
            else:
                entrys = merge_filter(field,args)
        
        elif isinstance(field,list):
            aux = []
            for val in field:
                aux +=merge_filter(val,args)
            entrys = merge_entrys(aux,entrys)
    
    return entrys

request = requests.get('http://services.web.ua.pt/parques/parques',timeout=40)
db_entrys = merge_filter(request.json(),1)
for entry in db_entrys:
    print(entry)

print('\n')
print('\n')
print('\n')

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

r = requests.get(url,headers={'Authorization': token},timeout=15)

db_entrys = merge_filter(r.json(),1)
mac_addresses = []
for entry in db_entrys:
    print(entry)
    if 'macAddress' in entry:
        mac_addresses.append(entry['macAddress'])

print(len(set(mac_addresses)))
print(len(mac_addresses))