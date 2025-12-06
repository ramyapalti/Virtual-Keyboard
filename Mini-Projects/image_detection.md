### When code runs,we have a background which shows only the change observed in that in binary format.

```import numpy as np
import cv2
cap=cv2.VideoCapture(0)
_, frame1 = cap.read()
_,frame2 = cap.read()
while(cap.isOpened()):
    diff=cv2.absdiff(frame1,frame2)
    gray= cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    _,thresh=cv2.threshold(gray,25,255,cv2.THRESH_BINARY)

    cv2.imshow("frame1",frame1)
    cv2.imshow("res",thresh)
    frame1=frame2
    ret,frame2=cap.read()
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```
