from requests import get, post
from datetime import datetime
from json import loads, dumps
from serial import Serial
from time import sleep

def send(msg):
    s.write(dumps(msg).replace("'", '"').encode('utf-8'))

def read(size):
    return s.read(size).decode('utf-8')

def now():
    dt = datetime.now()
    return f"{dt.day}.{dt.month} {dt.hour}:{dt.minute}"

s = Serial('/dev/rfcomm0', 9600, timeout = 1)

api_url = 'http://127.0.0.1:8000/api/'

api_gurl = api_url + 'getARobot'
api_purl = api_url + 'addARobot'
api_uurl = api_url + 'updateLatiLongF1F2'

send({'msg' : 'start'})

c = True

while (True):
    data = read(2048)

    while ('{' not in data):
        data += read(2048)

    data = data[data.index('{') :]

    while ('}' not in data):
        data += read(2048)

    ndata = data[: data.index('}') + 1]
    data = data[data.index('}') + 1 :]
    
    ndata = loads(ndata)

    ndata['f2'] = str(int(ndata['f2']) - 370)

    if (c):
        post(api_purl, json = {
            'lati' : 3633,
            'long' : 3034,
            'f1' : ndata['f1'],
            'f2' : ndata['f2']
        })

        with open('driver/flag.txt', 'w') as dest:
            dest.write('1')

        c = False
        print(1)
    else:
        post(api_uurl, json = {
            'lati' : 3633,
            'long' : 3034,
            'f1' : ndata['f1'],
            'f2' : ndata['f2']
        })

        print(ndata['f1'], ndata['f2'])

    tose = get(api_gurl).json()

    if (None == tose['perc']):
        tose['perc'] = '0'
    
    if (None == tose['fpsf']):
        tose['fpsf'] = '0'

    tose = {
        'perc' : tose['perc'],
        'fpsf' : tose['fpsf'],
        'noww' : now()
    }

    if (400 <= int(ndata['f1']) or 400 <= int(ndata['f2'])):
        tose['brea'] = 't'
    else:
        tose['brea'] = 'f'

    print(tose)

    send(tose)
    sleep(0.5)