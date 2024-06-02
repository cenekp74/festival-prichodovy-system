import json
import requests

SERVER_URL = 'http://127.0.0.1:7000/add'

with open("studenti.json", "r", encoding='utf-8') as f:
    students = json.load(f)

for student in students:
    name = student["jmeno"] + ' ' + student["prijmeni"]
    code = student["kod"]
    rfid = student["cip"]
    json_to_send = json.dumps({"name":name, "code":code, "rfid":rfid})
    requests.post(SERVER_URL, json=json_to_send)