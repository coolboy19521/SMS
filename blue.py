from requests import get, post
from json import loads, dumps
from serial import Serial
from time import sleep

def send(msg):
    s.write(dumps(msg).replace("'", '"').encode('utf-8'))

def read(size):
    return s.read(size).decode('utf-8')

s = Serial('/dev/rfcomm0', 9600, timeout = .5)

api_gurl = 'http://127.0.0.1:8000/api/getARobot'
api_purl = 'http://127.0.0.1:8000/api/addARobot'

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

    if (c):
        post(api_purl, json = {
            'lati' : ndata['lati'],
            'long' : ndata['long'],
            'f1' : ndata['f1'],
            'f2' : ndata['f2']
        })

        with open('driver/flag.txt', 'w') as dest:
            dest.write('1')

        c = False

    tose = get(api_gurl).json()
    tose = {
        'perc' : tose['perc'] or '0',
        'fpsf' : tose['fpsf'] or '0'
    }

    send(tose)
    sleep(0.5)