import requests 
import json

# tentar adicionar um daemon novo
print("_________________ ADD BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"url":"www.dated1.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD BASIC DAEMON REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"url":"www.dated2.pt"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD BASIC DAEMON REQUEST __________________")
args = {"1":"arg1","2":"arg2","3":["arg3","arg4","arg5"]}
r = requests.get('http://127.0.0.1:5000/Daemon/Add/Basic',{"url":"www.dated3.pt","args":json.dumps(args)},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
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
r = requests.get('http://127.0.0.1:5000/Daemon/Change/Basic/www.dated2.pt',{"args":json.dumps(args)},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
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