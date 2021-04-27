import requests 
import json

# listar todos os daemons
print("\n_________________ ALL REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/list_all')
print(r.status_code)
if r.status_code < 400:
    print(r.json())
print()

# tentar ver um daemon que existe
print("_________________ ID REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/2')
print(r.status_code)
print()

# tentar ver um daemon que não existe
print("_________________ NO ID REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/1')
print(r.status_code)
if r.status_code < 400:
    print(r.json())
print()

# alterar o url de um daemon
print("_________________ UPDATE URL REQUEST __________________")
r = requests.get('http://127.0.0.1:5000/Daemon/update_url/1',{"url":"www.updated.pt"})
print(r.status_code)
if r.status_code < 400:
    print(r.json())
print()

# tentar adicionar um daemon novo

    
# tentar dar update ao url de um daemon


# tentar adicionar outro daemon


# tentar obter a lista de todos os daemons


# tentar adicionar um daemon com um id que já existe 


# tentar apagar um daemon