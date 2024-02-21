from Module import FaceRecognizer, MainClass
from imutils.video import VideoStream

MainClass.WebcamControl = VideoStream(0, resolution = (640, 480), framerate = 20)
MainClass.Webcam = MainClass.WebcamControl.start()
Recognizer = FaceRecognizer()

Recognizer.CollectDataByCamera('Dataset', '0', 100)
Data = Recognizer.PrepareData('Dataset')

Recognizer.EigenFaceRecognizer.train(Data[0], Data[1])

Recognizer.EigenFaceRecognizer.write('Data/EigenFaceData/Data.xml')
Recognizer.EigenFaceRecognizer.read('Data/EigenFaceData/Data.xml')