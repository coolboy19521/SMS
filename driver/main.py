from Module import MainClass, HandDetector, FaceDetector, ColorDetector, CascadeObjectDetector, SSDObjectDetector, FaceRecognizer, PoseDetector
from cv2 import CascadeClassifier, VideoWriter, VideoWriter_fourcc, imshow, waitKey
from imutils.video import VideoStream
from threading import Thread
from os import listdir

MainClass.WebcamControl = VideoStream(0, resolution = (640, 480), framerate = 32)
MainClass.Webcam = MainClass.WebcamControl.start()

MainClass.LowerColor, MainClass.UpperColor = (32, 123, 53), (71, 215, 156)

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

MultiIndices = [5]
MainClass.Cascades = [CascadeClassifier('Data/Cascades/haarcascade_eye.xml'), CascadeClassifier('Data/Cascades/haarcascade_profileface.xml')]
MainClass.ColorValues = [[(41, 51, 48), (81, 255, 255)]]

MultiDetectors = [Detectors[Species[IndexSmall]] for IndexSmall in MultiIndices]

if (len(MultiIndices) > 1):
    In = VideoWriter(f'Videos/Mix/Input/{len(listdir(f"Videos/Mix/Input"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
    Out = VideoWriter(f'Videos/Mix/Output/{len(listdir(f"Videos/Mix/Output"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
else:
    In = VideoWriter(f'Videos/{Species[MultiIndices[0]]}/Input/{len(listdir(f"Videos/{Species[MultiIndices[0]]}/Input"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
    Out = VideoWriter(f'Videos/{Species[MultiIndices[0]]}/Output/{len(listdir(f"Videos/{Species[MultiIndices[0]]}/Output"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))

while (waitKey(1) & 0xFF != ord('q')):
    MainClass.FaceNotDetectedBBox = 1
    frame = MainClass.Webcam.read()
    In.write(frame)
    Threads = []

    MainClass.Log = [frame]
    MainClass.Angle = {}
    for Detector in MultiDetectors:
        frameToUse = frame.copy()
        # Detector(frameToUse)
        ThreadNow = Thread(target = Detector, args = (frameToUse, (1, 1)))
        Threads.append(ThreadNow)
        ThreadNow.start()

    for ThreadIndex in Threads:
        ThreadIndex.join()

    Out.write(MainClass.Log[0])
    print(MainClass.Angle)
    imshow("Matrix", MainClass.Log[0])

In.release()
Out.release()
MainClass.WebcamControl.stop()