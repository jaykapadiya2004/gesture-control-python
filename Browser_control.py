import cv2
import hand_tracker as hd
import pyautogui as auto
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

dec = hd.HandDetector(detectionCon=0.7)
p_time = time.time() - 1.5

while cap.isOpened():
    ret, img = cap.read()
    flip = cv2.flip(img, 1)
    finger1 = []
    cnt = 0

    hands, flip = dec.findHands(flip, flipType=True)
    if hands:
        hand1 = hands[0]
        lmlist1 = hand1["lmList"]
        bbox = hand1["bbox"]
        cp = hand1["center"]
        type1 = hand1["type"]

        finger1 = dec.fingersUp(hand1)
        for i in finger1:
            if i == 1:
                cnt += 1

        if type1 == "Left":
            if cnt == 2:
                length, info, img = dec.findDistance(lmlist1[8], lmlist1[4], flip)
                if length > 100:
                    auto.keyDown("Ctrl")
                    auto.scroll(60)
                    auto.keyUp("Ctrl")
                else:
                    auto.keyDown("Ctrl")
                    auto.scroll(-60)
                    auto.keyUp("Ctrl")
            elif cnt <= 1:
                if finger1[0] != 1:
                    length, info, flip = dec.findDistance(lmlist1[8], lmlist1[0], flip)
                    ratio = (length/bbox[2])*100
                    s = np.interp(ratio, [90, 210], [300, -300])
                    auto.scroll(int(s))
                else:
                    if time.time() - p_time >= 1.5:
                        auto.hotkey("browserforward")
                        p_time = time.time()
        elif type1 == "Right":
            if cnt == 2:
                pass

            elif cnt <= 1:
                if finger1[0] == 1:
                    if time.time() - p_time >= 1.5:
                        auto.hotkey("browserback")
                        p_time = time.time()
    
    cv2.imshow("IMG", flip)
    cv2.waitKey(1) 

cap.release()
cv2.destroyAllWindows()
