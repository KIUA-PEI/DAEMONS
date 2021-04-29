import requests
from consts import *

def data_wirelessUsers(token):
    print("teste")
    for dep in DEP:
        i = 0
        print("teste" + str(i))
        while i < MAX_AP[dep]:
            print("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/"+str(DEP[dep])+(str(i) if i >= 10 or i != 0 else "0" + str(i))+"/TotalUsernames")
            r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/"+\
            str(DEP[dep])+(str(i) if i >= 10 and i != 0 else "0" + str(i))+"/TotalUsernames", headers={'Authorization': token})
            print(r.status_code)
            print(r.text)
            i = i + 1


data_wirelessUsers('Bearer ' + "3e5de3f5-099a-3461-9bfa-4d0aa94ac264")