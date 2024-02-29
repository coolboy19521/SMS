from requests import get, post
from json import loads, dumps
from serial import Serial
from time import sleep

def send(msg):
    s.write(dumps(msg).encode('utf-8'))

def read(size):
    return loads(s.read(size).decode('utf-8'))

s = Serial('/dev/rfcomm0', 9600, timeout = 0.4)

api_gurl = '127.0.0.1:8000/api/getARobot'
api_purl = '127.0.0.1:8000/api/addARobot'

send({'msg' : 'start'})

c = True

while (True):
    data = read(2048)
    print(data)

    if (c):
        post(api_purl, json = {
            'lati' : data['lati'],
            'long' : data['long'],
            'f1' : data['f1'],
            'f2' : data['f2']
        })

        with open('driver/flag.txt', 'w') as dest:
            dest.write('1')

        c = False

    tose = get(api_gurl)

    send(tose)
    sleep(.5)