from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack, calcsize
from cv2 import imshow, waitKey
from threading import Thread
from pickle import loads

def Show():
    Data = b""
    LengthBytes = calcsize("Q")

    while(waitKey(1) & 0xFF != ord("q")):
        while(len(Data) < LengthBytes):
            Got = CacheClient.recv(4194304)
            Data = Data + Got

        Length = Data[: LengthBytes]
        Data = Data[LengthBytes :]
        MessageSize = unpack("Q", Length)[0]

        while(len(Data) < MessageSize):
            Data = Data + CacheClient.recv(4194304)

        Frame = loads(Data[: MessageSize])
        Data = Data[MessageSize :]

        imshow("Matrix", Frame)

    CacheClient.close()

CACHE_IP = "127.0.0.1"
CACHE_PORT = 5000
CACHE_BIND = (CACHE_IP, CACHE_PORT)

CacheClient = socket(AF_INET, SOCK_STREAM)
CacheClient.connect(CACHE_BIND)

Thread(target = Show).start()