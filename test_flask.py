import requests 
import json

# tentar adicionar um daemon novo
print("_________________ START ALL  __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Basic',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Basic',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Start/Key',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Key',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Start/Http',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Http',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Start/Http',{"id":3},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Http',{"id":4},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Start/Token',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Start/Token',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  



print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT TOKEN DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Token',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT HTTP DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Http',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT KEY DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Key',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  


print("_________________ REMOVE ALL __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Basic',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Basic',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Key',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Key',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Http',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Http',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"id":3},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"id":4},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ ADD WIFI TOKEN DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Token',{"id":1,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.get('http://127.0.0.1:5000/Daemon/Add/Token',{"id":2,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount_2_4GHz, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.get('http://127.0.0.1:5000/Daemon/Add/Token',{"id":3,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount_5GHz, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.get('http://127.0.0.1:5000/Daemon/Add/Token',{"id":4,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount_2_4GHz, upTime, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD KEY PARKING DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Key',{"id":1,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","args":"clientCount, location, macAddress"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD HTTP PARKING DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Http',{"id":1,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","username":"dummy","args":"clientCount, location, macAddress"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD PARKING BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"id":1,"url":"http://services.web.ua.pt/parques/parques","args":"Nome, Ocupado,Capacidade,Livre"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"id":2,"url":"http://services.web.ua.pt/parques/parques"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()
   
print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()   

"""
print("_________________ PAUSE BASIC __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Basic',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 

r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Key',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 

r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Http',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 

r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Token',{"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"id":2},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 


print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT TOKEN DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Token',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT HTTP DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Http',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  

print("_________________ PRINT KEY DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Key',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
"""


"""
print("_________________ PAUSE BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Pause/Basic/www.dated3.pt',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()   

print("_________________ REMOVE BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Basic',{"url":"www.dated3.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Token',{"url":"www.dated2.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print() 

r = requests.get('http://127.0.0.1:5000/Daemon/Remove/Basic',{"url":"www.dated1.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ CHANGE BASIC DAEMON args REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Change/Basic/www.dated2.pt',{"url":"www.dated3.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()   

print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)

if r.status_code < 400:
    print(r)
print()   

print("_________________ GET BASIC DAEMON FREQ5 REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Basic/Period/5',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()   

print("_________________ START __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Start/Basic',{'url':'http://services.web.ua.pt/parques/parques'},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()   


r = requests.get('http://127.0.0.1:5000/Daemon/Start/Token',{'url':'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  
"""