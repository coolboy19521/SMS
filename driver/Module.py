from cv2 import bitwise_and, bitwise_not, convexHull, cvtColor, fillConvexPoly, COLOR_BGR2RGB
from numpy import array, roll, zeros, uint8
from mediapipe.python import solutions

pose = solutions.pose
Pose = pose.Pose

class PoseDetector(Pose):
    def __init__(
        self,
        static_image_mode = True,
        model_complexity = 2,
        smooth_landmarks = False,
        enable_segmentation = False,
        smooth_segmentation = False,
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7
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

    def ProccessMultiple(self, Frame):
        frame = Frame.copy()
        cs = []

        while ((res := self.Process(frame))[0]):
            landmark_coords = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0]) + 10) for l in res[1]]

            hull = convexHull(array(landmark_coords))

            mask = zeros(frame.shape[:2], dtype = uint8)
            fillConvexPoly(mask, hull, (255))

            mask = bitwise_not(mask)
            ls = roll(mask, -100, axis = 1)
            rs = roll(mask, 100, axis = 1)
            us1 = roll(ls, -100, axis = 0)
            us2 = roll(rs, -100, axis = 0)
            us2 = roll(mask, -100, axis = 0)

            masks = [mask, ls, rs, us1, us2]

            for mask in masks:
                frame = bitwise_and(frame, frame, mask = mask)

            cs.append(self.FaceDot(frame, res[1]))

        return cs

    def Process(self, Frame):
        frame = cvtColor(Frame, COLOR_BGR2RGB)
        result_landmarks = self.process(frame).pose_landmarks

        if (result_landmarks):
            return True, result_landmarks.landmark

        return False, -1

    def FaceDot(self, frame, landmark):
        mxx, mxy, mnx, mny = -1, -1, 1e18, 1e18
        
        for i in range(10):
            mxx = max(mxx, landmark[i].x)
            mnx = min(mnx, landmark[i].x)
            mxy = max(mxy, landmark[i].y)
            mny = min(mny, landmark[i].y)

        mxx, mnx = int(mxx * frame.shape[1]), int(mnx * frame.shape[1])
        mxy, mny = int(mxy * frame.shape[0]), int(mny * frame.shape[0])

        cx, cy = mnx + (mxx - mnx) // 2, mny + (mxy - mny) // 2

        return cx, cy

    def Normalize(self, a, b, x):
        return max(min(x, b), a)