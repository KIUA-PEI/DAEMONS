import requests

def data_wirelessUsers():
    pass
    # r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint/deti-ap03/TotalUsernames")


def get_acess_token():
    request_token = requests.post('https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid', \
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'})
    if r.status_code == 200:
        return 'Bearer ' + request_token.json()['access_token']
