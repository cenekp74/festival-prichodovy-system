# pro pridani studentu z excel souboru se vsemi studenty na skole co jsem dostal od fajfra - asi na jedno pouziti
import json
import requests
import openpyxl

SERVER_URL = 'http://127.0.0.1:7000/add'

students = []
wb = openpyxl.open("SEZNAM.xlsx")
for sheet in wb.worksheets:
    for row in sheet.iter_rows(min_row=3, values_only=True):
        _, name, code = row
        students.append({"jmeno":name, "kod":code})

for student in students:
    name = student["jmeno"]
    code = student["kod"]
    json_to_send = json.dumps({"name":name, "code":code})
    requests.post(SERVER_URL, json=json_to_send)