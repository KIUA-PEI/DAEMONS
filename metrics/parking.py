import requests


def parking_data():
    r = requests.get("http://services.web.ua.pt/parques/parques")
    if r.status_code == 200:
        parking = r.json()
        timestamp = parking.pop(0)
        parking = [{"Nome":park["Nome"], "Capacidade" : park["Capacidade"], "Ocupado" : park["Ocupado"], "Livre" : park["Livre"]} for park in parking]
        parking.insert(0, timestamp)
    