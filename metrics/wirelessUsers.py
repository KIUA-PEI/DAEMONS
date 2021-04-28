import requests
from consts import *

def data_wirelessUsers(token):
    pass
    # for dep in DEP:
    #     i = 0
    #     while i < MAX_AP[dep]:
    #         r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/"+\
    #         str(DEP[dep])+(str(i) if i > 9 and not i == 0 else "0" + str(i))+"/TotalUsernames", headers={'Authorization': token})
    #         print(r.status_code)
    #         print(r.text)
    #         i = i + 1


# data_wirelessUsers('Bearer ' + "31ec0e34-0fc7-39a2-acd7-ef69715acda3")