import requests 
import json
#from influxdb import InfluxDBClient

"""
client = InfluxDBClient(database='dbname')
client = InfluxDBClient(host='127.0.0.1', port=8086, database='dbname')
client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='dbname')

# using UDP
client = InfluxDBClient(host='127.0.0.1', database='dbname', use_udp=True, udp_port=4444)
"""

#import pycurl
#       Host: https://wso2-gw.ua.pt
#       Context: /primecore_primecore-ws/1.0.0
#       Consumer key: j_mGndxK2WLKEUKbGrkX7n1uxAEa
#       Consumer secret: BrszH8oF9QsHRjiOAC1D9Ze0Iloa


#   curl --location --request POST 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid' \
#   --header 'Content-Type: application/x-www-form-urlencoded' \
#   --header 'Authorization: Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'


token = ''
i=0
while(1):
    i+=1
    #r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=2&firstResult=1', headers={'Authorization': token})
    #r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/Count', headers={'Authorization': token})
    #r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/10055300', headers={'Authorization': token})
    r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/Building', headers={'Authorization': token})
    
    print(r.status_code)
    print(r.headers)
    
    if r.status_code == 200:
        print('success')
        print(r.json())
        for building in r.json()['buildings']:
            new_request = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/NetworkMetric/ZTC?metric=tx&timeInterval=1',building, headers={'Authorization': token})
            print('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/NetworkMetric/%s?metric="rx"?timeinterval=1'%building)
            print(new_request.status_code)
            print(new_request.json())
            break
        break
    if r.status_code>400:
        if r.status_code == 401:
            print('get new token and repeat')
            request_token = requests.post('https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',
                                        headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'})
            print('token -> %s' % request_token.json()['access_token'])
            token = 'Bearer ' + request_token.json()['access_token']
            
        print('not good')
    
    if(i==2):
        break