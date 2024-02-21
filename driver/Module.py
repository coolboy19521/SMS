from cv2 import bitwise_and, inRange, findContours, contourArea, drawContours, moments, circle, line, COLOR_BGR2HSV, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, imencode, COLOR_BGR2GRAY, imwrite, resize, imread, rectangle, putText, FONT_HERSHEY_PLAIN, COLOR_BGR2RGB, CascadeClassifier, dnn_DetectionModel, FONT_HERSHEY_COMPLEX_SMALL, namedWindow, getTrackbarPos, createTrackbar, flip, imshow, resize, COLOR_GRAY2BGR
from cv2.face import EigenFaceRecognizer_create
from os import mkdir, listdir, walk, rename
from mediapipe.python import solutions
from string import ascii_lowercase
from imutils import grab_contours
from numpy import array, hstack
from math import sqrt, acos, pi
from random import choice

drawing_util = solutions.drawing_utils

hands = solutions.hands
Hands = solutions.hands.Hands

pose = solutions.pose
Pose = pose.Pose

LETTERS = ascii_lowercase

nothing = lambda x: 0

class MainClass():
    ConfigPath = "Data/SSD_Mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    WeightsPath = "Data/SSD_Mobilenet/frozen_inference_graph.pb"
    ClassNames = [name for name in open("Data/SSD_Mobilenet/coco.names", "r").read().split("\n")]
    FrontalFace = CascadeClassifier("Data/Cascades/haarcascade_frontalface_alt.xml")
    DataPath = 'Data/EigenFaceData/Data.xml'
    ColorValues = []
    Width, Height = None, None
    FaceNotDetectedBBox = 1
    ColorHSVValues = [None]
    FaceDetectorIndex = 0
    FrameOnProcess = None
    WebcamControl = None
    Cascades = None
    Webcam = None
    Tasks = []
    Angle = {}
    Log = []

    def FlaskFormat(self, frame):
        _, frame = imencode('.jpeg', frame)
        frame = frame.tobytes()

        return b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    
    def Process(self, Frame, Draw = (1, 1)):
        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)
        MainClass.Angle['Common'] = [- 90, 90]
        MainClass.Tasks.append((None, ))

        return Frame, None, [0]

class ColorDetector(MainClass):
    Count = 0

    def __init__(self):
        self.CountIndex = ColorDetector.Count
        ColorDetector.CountIndex = ColorDetector.Count + 1

    def Process(self, Frame, Draw = (1, 1), Action = 1, Tresh = 500, X = (640, 0), Y = (480, 0)):
        Hsv = cvtColor(Frame, COLOR_BGR2HSV)
        Centers, Areas = [], []

        MaskColor = inRange(Hsv, MainClass.ColorValues[self.CountIndex][0], MainClass.ColorValues[self.CountIndex][1])

        Contours = findContours(MaskColor, RETR_TREE, CHAIN_APPROX_SIMPLE)
        Contours = grab_contours(Contours)

        Angle = []

        for Contour in Contours:
            Area = contourArea(Contour)
            if (Area > Tresh):
                drawContours(Frame, [Contour], -1, (0, 255, 0), 2)
                M = moments(Contour)
                Areas.append(Area)
                CenterX = int(M["m10"] / M["m00"])
                CenterY = int(M["m01"] / M["m00"])

                Centers.append((CenterX, CenterY))

                if (Draw):
                    circle(Frame, (CenterX, CenterY), 7, (0, 0, 0), -1)
                    line(Frame, (320, 240), (CenterX, CenterY), (0, 0, 0), 2)

                if (Action and CenterX < X[0] and CenterX > X[1] and CenterY < Y[0] and CenterY > Y[1]):
                    Angle = [90, 0]

        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)

        MainClass.Angle['Color'] = Angle
        MainClass.Tasks.append((Centers, Areas))

        return Frame, Centers, Angle, Areas

class FaceDetector(MainClass):
    def Process(self, Frame, Draw = (0, 0), MinSize = (75, 75)):
        FrameGray = cvtColor(Frame, COLOR_BGR2GRAY)
        BBoxes = self.FrontalFace.detectMultiScale(FrameGray, 1.1, 6, minSize = MinSize)
        Faces = []

        if (Draw[0]):
            for BBox in BBoxes:
                if (len(BBox) > 0 and Draw[0]):
                    X, Y, W, H = BBox
                    Faces.append(Frame[Y : Y + H, X : X + W])

                    rectangle(Frame, (X, Y), (X + W, Y + H), (0, 0, 0), 2)
        else:
            for BBox in BBoxes:
                if (len(BBox) > 0):
                    X, Y, W, H = BBox
                    Faces.append(Frame[Y : Y + H, X : X + W])
        
        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)

        MainClass.Angle['Face'] = (len(Faces) > 0) * [- 90, 90]
        MainClass.Tasks.append((Faces, BBoxes))

        return Frame, Faces, (len(Faces) > 0) * [- 90, 90], BBoxes

    def DetectFaces(self, Frame, Draw = (0, 0), MinSize = (75, 75)):
        FrameGray = cvtColor(Frame, COLOR_BGR2GRAY)
        BBoxes = self.FrontalFace.detectMultiScale(FrameGray, 1.1, 6, minSize = MinSize)
        Faces = []

        if (Draw[0]):
            for BBox in BBoxes:
                if (len(BBox) > 0 and Draw[0]):
                    X, Y, W, H = BBox
                    Faces.append(FrameGray[Y : Y + H, X : X + W])

                    rectangle(Frame, (X, Y), (X + W, Y + H), (0, 255, 0), 2)
        else:
            for BBox in BBoxes:
                if (len(BBox) > 0):
                    X, Y, W, H = BBox
                    Faces.append(FrameGray[Y : Y + H, X : X + W])

        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)

        MainClass.Angle['Face'] = (len(Faces) > 0) * [- 90, 90]
        MainClass.Tasks.append((Faces, BBoxes))

        return Frame, Faces, (len(Faces) > 0) * [- 90, 90], BBoxes

class DataMaker(FaceDetector):
    def CollectDataByCamera(self, Path, Label = '0', DataSize = 300, RV = 0, OutputArray = [[]]):
        Index = 0

        try:
            mkdir(rf"{Path}/{Label}")

        except FileExistsError:
            pass

        if (not(RV)):
            while(Index < DataSize):
                Frame = self.Webcam.read()

                imwrite(rf"{Path}/{Label}/{Index}.jpg", Frame)

                Index = Index + 1
        else:
            while(Index < DataSize):
                Frame = self.Webcam.read()
                OutputArray[0] = Frame

                imwrite(rf"{Path}/{Label}/{Index}.jpg", Frame)

                Index = Index + 1

        return Path, rf"{Path}/{Label}"
    
    def PrepareWindow(self):
        namedWindow("Trackbars")

        createTrackbar("L - H", "Trackbars", 0, 179, nothing)
        createTrackbar("L - S", "Trackbars", 0, 255, nothing)
        createTrackbar("L - V", "Trackbars", 0, 255, nothing)
        createTrackbar("U - H", "Trackbars", 179, 179, nothing)
        createTrackbar("U - S", "Trackbars", 255, 255, nothing)
        createTrackbar("U - V", "Trackbars", 255, 255, nothing)

    def BruteForce(self, Frame):
        Frame = flip( Frame, 1 )

        hsv = cvtColor(Frame, COLOR_BGR2HSV)

        l_h = getTrackbarPos("L - H", "Trackbars")
        l_s = getTrackbarPos("L - S", "Trackbars")
        l_v = getTrackbarPos("L - V", "Trackbars")
        u_h = getTrackbarPos("U - H", "Trackbars")
        u_s = getTrackbarPos("U - S", "Trackbars")
        u_v = getTrackbarPos("U - V", "Trackbars")

        lower_range = array([l_h, l_s, l_v])
        upper_range = array([u_h, u_s, u_v])

        mask = inRange(hsv, lower_range, upper_range)

        res = bitwise_and(Frame, Frame, mask=mask)

        mask_3 = cvtColor(mask, COLOR_GRAY2BGR)

        stacked = hstack((mask_3, Frame, res))

        imshow('Trackbars', resize(stacked, None, fx=0.4, fy=0.4))

        MainClass.ColorHSVValues[0] = [(l_h,l_s,l_v), (u_h, u_s, u_v)]

    def PrepareData(self, Path, MinSize = (75, 75)):
        MainClass.WebcamControl.stop()
        Labels = [int(Label) for Label in listdir(Path)]
        FaceCollection = []
        FaceLabels = []

        for Label in Labels:
            RootPath = rf"{Path}/{Label}"
            Images = listdir(RootPath)
            Count = 1

            for ImageName in Images:
                ImagePath = rf"{RootPath}/{ImageName}"
                Image = imread(ImagePath)

                Faces = self.DetectFaces(Image, MinSize = MinSize)[1]

                if (len(Faces) > 0):
                    FaceResized = resize(Faces[0], (120, 120))
                    FaceLabels.append(Label)
                    FaceCollection.append(FaceResized)

                print(f'# {Count} / {len(Images)} -- ({Labels.index(Label) + 1} / {len(Labels)}) {ImageName}: Ready | Detected Face: {len(Faces) > 0}')
                Count = Count + 1

        return FaceCollection, array(FaceLabels)

class FaceRecognizer(DataMaker, MainClass):
    def __init__(self):
        self.EigenFaceRecognizer = EigenFaceRecognizer_create()
        self.EigenFaceRecognizer.read(self.DataPath)

    def Process(self, Frame, Draw = (1, 1), Tags = ["0"], Threshold = 0, MinSize = (75, 75)):
        _, DetectedFaces, _, BBoxes = self.DetectFaces(Frame, MinSize = MinSize)
        TagsFound = []

        for Index in range(len(DetectedFaces)):
            DetectedFace, BBox = DetectedFaces[Index], BBoxes[Index]
            ResizedFace = resize(DetectedFace, (120, 120))
            LabelFace = self.EigenFaceRecognizer.predict(ResizedFace)

            X, Y, W, H = BBox

            if (LabelFace[1] > Threshold):
                TagFace = f"{Tags[LabelFace[0]]}: {int(LabelFace[1])}"
            else:
                TagFace = 'Unknown'

            TagsFound.append(TagFace)

            if (Draw[0]):
                rectangle(Frame, (X, Y), (X + W, Y + H), (0, 0, 0), 2)
                putText(Frame, TagFace, (X, Y - 20), FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1)
        
        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)

        MainClass.Angle['FaceRecognize'] = (len(TagsFound) > 0) * [- 90, 90]
        MainClass.Tasks.append((TagsFound, ))

        return Frame, TagsFound, (len(TagsFound) > 0) * [- 90, 90]

class HandDetector(Hands, MainClass):
    def __init__(
        self,
        static_image_mode = 0,
        max_num_hands = 4,
        model_complexity = 1,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5
    ):
        super().__init__(
            static_image_mode,
            max_num_hands,
            model_complexity,
            min_detection_confidence,
            min_tracking_confidence
        )

    def Process(self, Frame, Draw = (0, 0), Apply = 0):
        frame = cvtColor(Frame, COLOR_BGR2RGB)
        height, width = frame.shape[: 2]
        multi_landmarks = self.process(frame).multi_hand_landmarks
        bbox_array = []
        returnedValue = 0

        indices = {}

        if (multi_landmarks):
            returnedValue = 1
            for index, hand in enumerate(multi_landmarks):
                max_x, min_x = 0, 1e5
                max_y, min_y = 0, 1e5
                indices[index] = {}
                for index_landmark, landmark in enumerate(hand.landmark):
                    indices[index][index_landmark] = (landmark.x, landmark.y)
                    array = indices[index][index_landmark]
                    if (array[0] > max_x):
                        max_x = array[0]
                    elif (array[0] < min_x):
                        min_x = array[0]
                    if (array[1] > max_y):
                        max_y = array[1]
                    elif (array[1] < min_y):
                        min_y = array[1]

                center_x, center_y = int((min_x + max_x) * width / 2), int((min_y + max_y) * height / 2)
                if (Draw[0] and Draw[1]):
                    rectangle(Frame, (int(min_x * width), int(min_y * height)), (int(max_x * width), int(max_y * height)), (255, 0, 0))
                    circle(Frame, (center_x, center_y), 5, (0, 255, 0), -1)
                    drawing_util.draw_landmarks(Frame, hand, hands.HAND_CONNECTIONS)
                elif (Draw[0]):
                    drawing_util.draw_landmarks(Frame, hand)

                bbox_array.append(((max_x, min_x), (max_y, min_y), (center_x, center_y)))

        if (Apply):
            if (len(MainClass.Log) > 0):
                MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
            else:
                MainClass.Log.append(Frame)
            MainClass.Tasks.append((indices, bbox_array))

        MainClass.Angle['Hand'] = returnedValue * [90, 0]
        return Frame, indices, returnedValue, bbox_array
    
    def ProcessAngle(self, Frame, Draw = (1, 1)):
        Result = self.Process(Frame, Draw, 0)
        Angle = [0, 0]
        if (Result[2]):
            Height, Width = Frame.shape[: 2]
            PointX = Result[3][0][2][0]
            PointY = Result[3][0][2][1]
            TargetX = Result[1][0][0][0] * Width
            TargetY = Result[1][0][0][1] * Height
            line(Result[0], (PointX, PointY), (int(TargetX), int(TargetY)), (0, 0, 255), 2)
            line(Result[0], (PointX, int(TargetY)), (int(TargetX), int(TargetY)), (0, 0, 255), 2)
            circle(Result[0], (PointX, int(TargetY)), 5, (0, 255, 0), -1)
            X = PointX - TargetX
            Y = PointY - TargetY
            Magnitude = sqrt(X * X + Y * Y)
            if (Magnitude > 0):
                AngleInt = acos(X / Magnitude)
            AngleInt = AngleInt * 180 / pi
            if (Y < 0):
                AngleInt = 180 - AngleInt

            Angle = [int(AngleInt)]

        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Result[0])
        else:
            MainClass.Log.append(Result[0])

        MainClass.Angle['HandAngle'] = Result[2] * Angle
        MainClass.Tasks.append((Result[1], Result[3]))

        return Result

class PoseDetector(Pose, MainClass):
    def __init__(
        self,
        static_image_mode = False,
        model_complexity = 1,
        smooth_landmarks = True,
        enable_segmentation = False,
        smooth_segmentation = True,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5
    ):
        super().__init__(
            static_image_mode,
            model_complexity,
            smooth_landmarks,
            enable_segmentation,
            smooth_segmentation,
            min_detection_confidence,
            min_tracking_confidence
        )

    def Process(self, Frame, Draw = (0, 0)):
        frame = cvtColor(Frame, COLOR_BGR2RGB)
        result_landmarks = self.process(frame).pose_landmarks
        returnedValue = 0

        indices = {}

        if (result_landmarks):
            returnedValue = 1
            for index, member in enumerate(result_landmarks.landmark):
                indices[index] = (member.x, member.y)

        if (Draw[0] and Draw[1]):
            drawing_util.draw_landmarks(Frame, result_landmarks, pose.POSE_CONNECTIONS)
        elif (Draw[0]):
            drawing_util.draw_landmarks(Frame, result_landmarks)

        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log.append(Frame)

        MainClass.Angle['Pose'] = returnedValue * [-90, 90]
        MainClass.Tasks.append((indices, ))

        return Frame, indices, returnedValue


class BasicDataCollector():
    def generateRandom(self, length):
        new_name = "".join([choice(LETTERS) for _ in range(length)])

        return new_name

    def renameRandom(self, path, endswith, length):
        folder = walk(path)

        for _, _, images in folder:
            for image in images:
                flag = 0
                for ending in endswith:
                    if (image.endswith(f".{ending}")):
                        flag = 1
                if (flag):
                    new_name = self.generateRandom(length)

                    while(new_name in images):
                        new_name = self.generateRandom(length)

                    rename(f"{path}\\{image}", f"{path}\\{new_name}.{endswith[0]}")

class CascadeObjectDetector(MainClass):
    Count = 0

    def __init__(self):
        self.CascadeIndex = CascadeObjectDetector.Count
        CascadeObjectDetector.Count = CascadeObjectDetector.Count + 1

    def Process(self, Frame, Draw = (1, 1), ScaleFactor = 1.05, MinNeighbors = 6, Color = (0, 255, 0), X = 640, Y = 480, MinSize = (100, 100)):
        original_sizes = Frame.shape[: 2]
        pos_arr = []

        frame = resize(Frame, (X, Y))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        flags_found = self.Cascades[self.CascadeIndex].detectMultiScale(gray, ScaleFactor, MinNeighbors, minSize = MinSize)

        for (x, y, w, h) in flags_found:
            x = int(x / X * original_sizes[1])
            y = int(y / Y * original_sizes[0])

            w = int(w / X * original_sizes[1])
            h = int(h / Y * original_sizes[0])

            rectangle(Frame, (x, y), (x + w, y + h), Color, 2) if (Draw[0]) else None
            pos_arr.append((x, y, w, h))
        
        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)

        MainClass.Angle['CascadeObject'] = (len(flags_found) > 0) * [- 90, 90]
        MainClass.Tasks.append((pos_arr, ))

        return Frame, pos_arr, (len(flags_found) > 0) * [- 90, 90]

class SSDObjectDetector(dnn_DetectionModel, MainClass):
    def __init__(self):
        super().__init__(self.ConfigPath, self.WeightsPath)

        self.Setup()

    def Setup(self):
        self.setInputSize(320, 320)
        self.setInputScale(1 / 127.5)
        self.setInputMean((127.5, 127.5, 127.5))
        self.setInputSwapRB(1)

    def Process(self, Frame, Draw = (1, 1), Thres = 0.5):
        classIDs, confs, bboxes = self.detect(Frame, confThreshold = Thres)

        if (Draw[0] and len(classIDs) > 0):
            for classID, conf, bbox in zip(classIDs.flatten(), confs.flatten(), bboxes):
                width, height = bbox[: 2]
                x, y = bbox[2 : 4]

                rectangle(Frame, (width, height), (width + x, height + y), (255, 0, 0), 2)
                putText(Frame, f"{self.ClassNames[classID - 1]} {int(conf * 100)}%", (width + 10, height + 20), FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)

        if (len(MainClass.Log) > 0):
            MainClass.Log[0] = bitwise_and(MainClass.Log[0], Frame)
        else:
            MainClass.Log = [Frame]

        MainClass.Angle['SSDObject'] = (len(classIDs) > 0) * [- 90, 90]
        MainClass.Tasks.append((classIDs, classIDs, bboxes))

        return Frame, classIDs, (len(classIDs) > 0) * [- 90, 90], classIDs, bboxes