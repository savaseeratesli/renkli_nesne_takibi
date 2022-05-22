import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

pinMode=12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinMode,GPIO.OUT)
pwm=GPIO.PWM(pinMode,50)#50 datasheet
pwm.start(0)

cam=cv2.VideoCapture(0)
#Cam ayarları
cam.set(3,320.0)
cam.set(4,240.0)

rows,cols=cam.get(4),cam.get(3)
#Sağ Sol 
center=int(cols/2)#Görüntü merkezi
x_ortalama=int(cols/2)#Nesne merkezi
position=90
sapma=30

#Servo döndürme
def SetAngle(angle):
    duty=angle/18+2
    pwm.ChangeDutyCycle(duty)
    sleep(0.05)
    pwm.ChangeDutyCycle(0)

#Nesne bulma,contour ile
def filt(img,low=np.array([160,155,85]),high=np.array([180,255,255])):#Kırmızı renk
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hsv=cv2.inRange(hsv,low,high)
    
    contours,_=cv2.findContours(hsv,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)#Büyükten küçüğe sıralama
    return contours


while cam.isOpened():
    _,frame=cam.read()
    
    contours=filt(frame)
    
    #Orta çizgi yanında takip çizgisi video ortası nesne ortası
    for cnt in contours:
        x,y,w,h=cv2.boundingRect(cnt)
        x_ortalama=int(x+w/2)
        break
    
    if x_ortalama<center-sapma:
        if position<180:
            position+=1
            SetAngle(position)
        
    elif x_ortalama>center+sapma:
        if position>0:
            position-=1
            SetAngle(position)
            
    print(position)
    
    cv2.line(frame,(x_ortalama,0),(x_ortalama,300),(0,255,255),3)
    cv2.line(frame,(center,0),(center,300),(0,0,255),3)
    cv2.imshow("Frame",frame)
    

    if cv2.waitKey(33)==ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()










