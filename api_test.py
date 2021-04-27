import requests 
import json
#import pycurl
#       Host: https://wso2-gw.ua.pt
#       Context: /primecore_primecore-ws/1.0.0
#       Consumer key: j_mGndxK2WLKEUKbGrkX7n1uxAEa
#       Consumer secret: BrszH8oF9QsHRjiOAC1D9Ze0Iloa


#   curl --location --request POST 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid' \ --header 'Content-Type: application/x-www-form-urlencoded' \ --header 'Authorization: Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'
def get_acess_token():
    request_token = requests.post('https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid', \
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'})
    print('new token -> %s' % request_token.json()['access_token'])
    
    return 'Bearer ' + request_token.json()['access_token']

token = get_acess_token()

def explore_access_points():
    # print(r.text)
    # print(r.headers)

    r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=700', headers={'Authorization': token})

    acess_points = json.loads(r.text)

    # print(acess_points["accessPoints"])

    for ap in acess_points["accessPoints"]:
        print(ap["name"])
        try:
            if ap["name"].find("deti") != -1 or ap["location"].find("deti") != -1:
                print(str(ap) + "\n")

            if ap["name"].find("biblioteca") != -1 or ap["location"].find("biblioteca") != -1:
                print(str(ap) + "\n")

        except Exception:
            print("ap name not string")
            print("-->" + ap["name"])

    ## SECALHAR RECOLHER SÓ AS INFORMAÇÕES RELATIVAS AOS ACCESS POINTS DO DETI,E DA BIBLIOTECA
    # ap["name"] do deti vai do deti-ap01 até deti-ap23
    # ap["name"] da biblioteca vai do biblioteca-ap01 até biblioteca-ap26

def main():
    explore_access_points()
    

main()