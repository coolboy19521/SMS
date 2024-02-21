from socket import socket, AF_INET, SOCK_STREAM
from imutils.video import VideoStream
from pickle import dumps, loads
from threading import Thread
from struct import pack

# def SendPieces(Client, FullData, N):
#     Pre = 0
#     for _ in range(N):
#         Client.sendall(FullData[Pre : Pre + (len(FullData) - len(FullData) // N)])
#         Pre = Pre + (len(FullData) - len(FullData) // N)

def Recieve():
    try:
        while(1):
            Angle = Client.recv(1024)
            print(loads(Angle))
    except Exception:
        return 0

def Serve():
    try:
        for _ in range(Count):
            CurFrame = Cam.read()
            Transformed = dumps(CurFrame)
            MessageFrame = pack("Q", len(Transformed)) + Transformed

            Client.sendall(MessageFrame)

            # Client.send(MessageFrame[: len(MessageFrame) // 4])
            # Client.send(MessageFrame[len(MessageFrame) // 4 : len(MessageFrame) - (len(MessageFrame) // 4) * 2])
            # Client.send(MessageFrame[len(MessageFrame) - (len(MessageFrame) // 4) * 2 : len(MessageFrame) - len(MessageFrame) // 4])
            # Client.send(MessageFrame[len(MessageFrame) - len(MessageFrame) // 4 :])
            # Client.sendall(MessageFrame)
            # SendPieces(Client, pack("Q", len(dumps(Cam.read()))) + dumps(Cam.read()), 8)
    except OSError:
        Network.close()

    CamController.stop()

IP = "127.0.0.1"
PORT = 5000
BIND = (IP, PORT)

Network = socket(AF_INET, SOCK_STREAM)
Network.bind(BIND)
Network.listen(1)

CamController = VideoStream(0, resolution = (640, 480), framerate = 32)
Cam = CamController.start()

Count = int(1e3)

Client, _ = Network.accept()


Thread(target = Serve).start()
Thread(target = Recieve).start()