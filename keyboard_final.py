import cv2
import numpy as np
import imutils

def intial(image):
    temp = image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 71, 7)
    blur = cv2.GaussianBlur(thresh, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)
    contours, heirarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # To detect the biggest square
            pts = np.float32([[ 102, 66],[ 958,  74],[77, 478],[973,  486]])
            screenpts = np.float32([[0, 0], [999, 0], [0, 599], [999, 599]])
            matrix = cv2.getPerspectiveTransform(pts, screenpts)
            global result
            result = cv2.warpPerspective(thresh, matrix, (1000, 600))
    return (result)

datasmall = np.array([['!','@','#','$','%','^','&','*','(',')'],
             ['1','2','3','4','5','6','7','8','9','0'],
             ['q','w','e','r','t','y','u','i','o','p'],
             ['a','s','d','f','g','h','j','k','l',' '],
             ['z','x','c','v','b','n','m','','',''],
             [':',';','"','`',',','.','<','>','/','?']])
datacaps =  np.array([['!','@','#','$','%','^','&','*','(',')'],
             ['1','2','3','4','5','6','7','8','9','0'],
             ['Q','W','E','R','T','Y','U','I','O','P'],
             ['A','S','D','F','G','H','J','k','L',''],
             ['Z','X','C','V','B','N','M','','',''],
             [':',';','"','`',',','.','<','>','/','?']])
string = ""

a= [None]*10000
b= [None]*10000
def is_click(c1,c2,i, t):
    isclick=0
    c1= int(c1/100)
    c2= int(c2/100)
    a[i-1]=c1
    b[i-1]=c2
    p=7
    if(i>p) :
        j=i
        v=0
        while(j>i-p) :
            if(a[j-1]== a[j-p] and b[j-1] == b[j-p]):
                v=v+1
            j=j-1
        if(v==p):
            isclick=1
    q=12
    if (i > q):
        j = i
        v = 0
        while (j > i - q):
            if (a[j - 1] == a[j - q] and b[j - 1] == b[j - q]):
                v = v + 1
            j = j - 1
        if (v == q):
            isclick = 2
    return isclick
def letter_reader( c1 ,c2, caps):
    x1= int(c1/100)
    y1= int(c2/100)
    if (c1>900 and c1 <= 1000 and c2 > 300 and c2 <= 400):
        return 0
    else :
        if(c1>900 and c1<=1000 and c2>400 and c2<=500):
            return 1
        else :
            if (c1 > 700 and c1 <= 9000 and c2 > 400 and c2 <= 500):
                return 2
            else :
                if (caps==0):
                    return datasmall[y1][x1]
                if (caps==1):
                    return datacaps[y1][x1]
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 100)
ret, frame = cap.read()
frame= cv2.resize(frame, (1000,600))
res= intial(frame)
i=1
temp1=''
v=0
t=0
q=0
while True:
    output= np.ones((512, 512, 1), dtype = "uint8")
    output.fill(255)
    ret, frame2= cap.read()
    frame2= cv2.resize(frame2, (1000,600))
    cv2.imshow('frame', frame2)
    res1= intial(frame2)
    diff0 = cv2.absdiff(res, res1)
    median= cv2.medianBlur(diff0, 9)
    gray= median
    kernal= np.ones((1,2), np.uint8)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray= cv2.medianBlur(gray, 9)
    thresh = cv2.dilate(gray, kernal, iterations=10)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if cnts!=[] :
        c = max(cnts, key=cv2.contourArea)
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        cv2.drawContours(res1, [c], -1, (0, 255, 255), 2)
        cv2.circle(res1, extTop, 8, (255, 0, 0), -1)
        cv2.imshow("Image", res1)
        click= is_click(extTop[0], extTop[1],i, t)
        if(click==1) :
            l= letter_reader(extTop[0], extTop[1], 0)
            if(temp1!=l):
                q=1
                if(l==1):
                    string= string[:-1]
                else :
                    if (l==0):
                        string= string+"|"
                    else :
                        if(l==2) :
                            string= string +" "
                            print("yes")
                        else :
                            string=string + l
            t=i
            if(q==1):
                temp1= l
            t=t+1
        if (click == 2):
            l = letter_reader(extTop[0], extTop[1], 1)
            if (temp1!=l):
                q=1
                if (l == 1):
                    string = string
                else:
                    if (l == 0):
                        string = string
                    else:
                        if (l == 2):
                            string = string + " "
                            print("yes")
                        else:
                            string = string[:-1] + l
            t=i
            if(q==1):
                temp1 = l
            t=t+1
        cv2.putText(output, string, (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Output', output)
    i=i+1
    if not ret:
        continue
    key= cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()