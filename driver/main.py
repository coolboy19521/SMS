from cv2 import imshow, waitKey, circle, putText, FONT_HERSHEY_COMPLEX_SMALL
from Module import MainClass, PoseDetector
from imutils.video import VideoStream

MainClass.WebcamControl = VideoStream(0, resolution = (640, 480), framerate = 20)
MainClass.Webcam = MainClass.WebcamControl.start()

det = PoseDetector().ProccessMultiple

while (waitKey(5) != ord('q')):
    frame = MainClass.Webcam.read()

    cs = det(frame)

    for ix, (cx, cy) in enumerate(cs):
        circle(frame, (cx, cy), 50, (0, 0, 255), 1)
        putText(frame, f"{ix}", (cx - 25, cy + 25), 1, FONT_HERSHEY_COMPLEX_SMALL, (0, 0, 0), 1)

    imshow("Matrix", frame)

MainClass.WebcamControl.stop()