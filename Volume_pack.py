import cv2
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from numpy import interp

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]


def set_volume(mylist, img):

    lmList = mylist

    if lmList != []:
        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]

        cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        vol = interp(length, [20, 170], [volMin, volMax])
        volume.SetMasterVolumeLevel(vol, None)
        
    return img
