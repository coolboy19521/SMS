import cv2
import time
import requests

URL = "http://192.168.206.120"
AWB = True

cap = cv2.VideoCapture(URL + ":81/stream")

def set_resolution(url: str, index: int=1, verbose: bool=False):
    try:
        if verbose:
            resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")

if __name__ == '__main__':
    set_resolution(URL, index=5)

    s = time.time()

    while cap.isOpened() and cv2.waitKey(1) != ord('q'):
        ret, frame = cap.read()
        e = time.time()

        cv2.putText(frame, f'{1 / (e - s)}', (20, 20), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 0), 1)
        cv2.imshow("frame", frame)
        s = e

    cv2.destroyAllWindows()
    cap.release()