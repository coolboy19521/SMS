from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc, destroyAllWindows, imshow, waitKey, circle, putText, FONT_HERSHEY_COMPLEX_SMALL
from Module import PoseDetector
from requests import post
from math import sqrt, ceil
from time import time
from os import listdir

def dis(l, r):
    x1, y1 = l
    x2, y2 = r

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

flag = False

while (not flag):
    with open('flag.txt', 'r') as dest:
        flag = int(dest.read())

with open('flag.txt', 'w') as dest:
    dest.write('0')

wrtr = VideoWriter(f'videos/video_{len(listdir("videos"))}.avi', VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))

api_url = "http://127.0.0.1:8000/api/updatePercFpsf"
url = "rtsp://admin:BRGOII@192.168.247.55:554/Streaming/Channels/102"

cam = VideoCapture(url + ':81/stream')

det = PoseDetector().ProccessMultiple
d, nc, h, f = [], {}, 0, 0

s = time()
inf = 1e18

while (waitKey(1) != ord('q')):
    _, frame = cam.read()

    cs = det(frame)

    bet = {e : (None, 1e18) for e in d}
    sta = {c : None for c in cs}
    ps = []

    for _ in range(len(cs)):
        for c in cs:
            md, p = 1e18, None

            for e in d:
                if (dis(c, e) < md and dis(c, e) < bet[e][1]):
                    md, p = dis(c, e), e

            if (None != p):
                if (bet[p][1] < inf):
                    sta[bet[p][0]] = None

                bet[p] = (c, md)
                sta[c] = p

    for e in sta:
        if (None != sta[e]):
            d.remove(sta[e])
            d.append(e)

            ps.append(e)

    for e in d:
        if (e not in ps):
            nc[e] += 1
        else:
            if (sta[e] in nc):
                nc.pop(sta[e])
                nc[e] = 0

    for e in d:
        if (10 == nc[e]):
            if (dis(e, (640, 480)) < dis(e, (0, 0))):
                h += 1
            else:
                h -= 1

    d = [e for e in d if (10 != nc[e])]
    nc = {k : nc[k] for k in nc if (nc[k] != 10)}

    for e in sta:
        if (None == sta[e]):
            d.append(e)
            nc[e] = 0

    for ix, (cx, cy) in enumerate(cs):
        circle(frame, (cx, cy), 50, (0, 0, 255), 1)
        putText(frame, f"{ix}", (cx - 25, cy + 25), 1, FONT_HERSHEY_COMPLEX_SMALL, (0, 0, 0), 1)

    h = max(h, 0)
    e = time()
    f = ceil(1 / (e - s))
    s = e

    putText(frame, f"H: {h}, D: {len(d)}, F: {f}", (50, 100), 1, FONT_HERSHEY_COMPLEX_SMALL, (0, 0, 0), 1)

    wrtr.write(frame)
    imshow("Matrix", frame)

    post(api_url, json = {
        'perc' : h,
        'fpsf' : f,
    })

cam.release()
destroyAllWindows()