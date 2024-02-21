from Module import ColorDetector, HandDetector, MainClass, PoseDetector, FaceRecognizer, FaceDetector, SSDObjectDetector, CascadeObjectDetector
from cv2 import CascadeClassifier, VideoWriter_fourcc, VideoWriter, imshow, waitKey
from socket import socket, AF_INET, SOCK_STREAM
from struct import calcsize, pack, unpack
from pickle import dumps, loads
from threading import Thread
from numpy import zeros
from os import listdir

def SendPieces(Client, FullData, N):
    Pre = 0
    for _ in range(N):
        Client.sendall(FullData[Pre : Pre + (len(FullData) - len(FullData) // N)])
        Pre = Pre + (len(FullData) - len(FullData) // N)

def BinaryFormat(Frame):
    Transformed = dumps(Frame)
    MessageFrame = pack("Q", len(Transformed)) + Transformed

    return MessageFrame

def GetAndProcessFrame(Indices):
    MultiDetectors = [Detectors[Species[IndexSmall]] for IndexSmall in Indices]
    CacheClient = socket(AF_INET, SOCK_STREAM)
    CacheClient.connect(CACHE_BIND)
    LengthBytes = calcsize("Q")
    Threads = []
    Data = b""

    if (len(Indices) > 1):
        In = VideoWriter(f'Videos/Mix/Input/{len(listdir(f"Videos/Mix/Input"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
        Out = VideoWriter(f'Videos/Mix/Output/{len(listdir(f"Videos/Mix/Output"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
    else:
        In = VideoWriter(f'Videos/{Species[Indices[0]]}/Input/{len(listdir(f"Videos/{Species[Indices[0]]}/Input"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
        Out = VideoWriter(f'Videos/{Species[Indices[0]]}/Output/{len(listdir(f"Videos/{Species[Indices[0]]}/Output"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))

    for _ in range(Count):
        MainClass.Angle = {}
        MainClass.Tasks = []
        MainClass.Log = [0]

        while (len(Data) < LengthBytes):
            Got = CacheClient.recv(4194304)
            Data = Data + Got

        Length = Data[: LengthBytes]
        Data = Data[LengthBytes :]
        MessageSize = unpack("Q", Length)[0]

        while (len(Data) < MessageSize):
            Data = Data + CacheClient.recv(4194304)

        FrameData = Data[: MessageSize]
        FrameNumpy = loads(FrameData)

        In.write(FrameNumpy)
        FrameMain = FrameNumpy.copy()
        MainClass.Log = [FrameNumpy]
        for Detector in MultiDetectors:
            FrameLoop = FrameMain.copy()
            # Detector(FrameLoop, Draw = (1, 1))
            OutputThread = Thread(target = Detector, args = (FrameLoop, (1, 1)))
            Threads.append(OutputThread)
            OutputThread.start()

        for UniThread in Threads:
            UniThread.join()

        Output = MainClass.Log
        FrameResult = Output[0]
        Out.write(FrameResult)
        Data = Data[MessageSize :]

        imshow("Matrix", FrameResult)

        if (waitKey(1) & 0xFF == ord('q')):
            break

        CacheClient.send(dumps(MainClass.Angle))

        Index[0] = Index[0] + 1

    CacheClient.close()
    In.release()
    Out.release()


Species = {
    0 : 'Common',
    1 : 'ColorDetector',
    2 : 'CascadeObjectDetector',
    3 : 'FaceDetector',
    4 : 'FaceRecognizer',
    5 : 'PoseDetector',
    6 : 'SSDObjectDetector',
    7 : 'HandDetector',
    8 : 'HandDetectorAngle'
}

Detectors = {
    'Common' : MainClass().Process,
    'ColorDetector' : ColorDetector().Process,
    'CascadeObjectDetector' : CascadeObjectDetector().Process,
    'FaceDetector' : FaceDetector().Process,
    'FaceRecognizer' : FaceRecognizer().Process,
    'PoseDetector' : PoseDetector().Process,
    'SSDObjectDetector' : SSDObjectDetector().Process,
    'HandDetector' : HandDetector().Process,
    'HandDetectorAngle': HandDetector().ProcessAngle
}

MainClass.Cascades = [CascadeClassifier('Data/Cascades/haarcascade_profileface.xml'), CascadeClassifier('Data/Cascades/haarcascade_eye.xml'), CascadeClassifier('Data/Cascades/haarcascade_frontalface_alt.xml')]

CACHE_IP = "127.0.0.1"
CACHE_PORT = 5000
CACHE_BIND = (CACHE_IP, CACHE_PORT)

ClientIndex = [1]
Frame = [pack("Q", len(dumps(zeros((480, 640, 3))))) + dumps(zeros((480, 640, 3)))]
Index = [0]

MainClass.ColorValues = [[(92, 49, 105), (121, 255, 255)]]

Count = int(1e3)
MultiIndices = [3]

GetAndProcessFrame(MultiIndices)