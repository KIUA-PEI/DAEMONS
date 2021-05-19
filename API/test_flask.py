import requests 
import json

# tentar adicionar um daemon novo
print("_________________ PRINT BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Print/Basic',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()  


print("_________________ ADD WIFI TOKEN DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Token',{"url":"www.dated2.pt","args":"first,count,clientCount,macAddress,location","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD PARKING BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"url":"http://services.web.ua.pt/parques/parques","args":"Nome,Capacidade,Ocupado,Livre"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
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
