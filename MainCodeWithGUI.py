import cv2
from tkinter import*
from PIL import Image, ImageTk
import mediapipe as mp
import time as time
import numpy as np
import math as m


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def findDis(x,y):
    dist = m.sqrt((x[1]-x[0])**2+(y[1]-y[0])**2)
    return dist



win = Tk()
win.geometry("1280x960")
#tkinter Window
win.title("Walk Analysis Window")
frame_1 = Frame(win, width=1280, height=920, bg="#00001a").place(x=0, y=0)
w = 700
h = 620
label1 = Label(frame_1, width=w, height=h)
label1.place(x=10, y=160)
var1 = IntVar()

Label(win,text="Walk Analyst",font=("Monoton",30),bg="#04FCE5").place(x=520,y=0)
Label(win,text="Select a Video",font=("Times",25),bg="#E6BE09").place(x=1000,y=100)
VIDEOS=[("Video 1","Old_1.mp4",1000,200),
        ("Video 2","Adult_2.mp4",1000,240),
        ("Video 3","Adult_3.mp4",1000,280),
        ("Video 4","Adult_4.mp4",1000,320),
        ("Video 6","Adult_5.mp4",1000,360),
        ("Video 7","Child_1.mp4",1000,400),
        ("Video 8","Child_2.mp4",1000,440),
        ("Video 9","Child_3.mp4",1000,480),
        ("Video 10","Injured_1.mp4",1000,520),
        ("Video 11","Injured_2.mp4",1000,560),
        ("Video 12","Injured_3.mp4",1000,600),
        ("Video 13","Injured_4.mp4",1000,640),
        ("Video 14","Injured_5.mp4",1000,680),
        ("Video 15","Adult_1.mp4",1000,720),
]
v_address=StringVar()
v_address.set("Adult_1.mp4")
live_v=IntVar()
live_v.set(1)
def video_click(address):
    global cap
    if address==0:
        print("0")
        cap = cv2.VideoCapture(0)
        v_address.set("")
    else:
        v_address.set(address)
        cap = cv2.VideoCapture(v_address.get())
for name,address,x,y in VIDEOS:
    Radiobutton(win,text=name,variable=v_address,value=address).place(x=x,y=y)
Button(win,text="Play",command=lambda:video_click(v_address.get())).place(x=1100,y=200)
# Live and Recorded video switching 
Label(win,text="Select Mode",font=("Times",25),bg="#0196FD").place(x=750,y=480)
Radiobutton(win,text="Live Camera",variable=live_v,value=0).place(x=750,y=560)
Button(win,text="Select",bg="white",command=lambda:video_click(live_v.get())).place(x=750,y=600)

cap = cv2.VideoCapture("Adult_2.mp4")



def WalkAnalyst(frame):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pTime=0
    cTime=0
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make detection
        results = pose.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    try:
        landmarks = results.pose_landmarks.landmark
        # Get coordinates
        nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y]
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        rheel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        # calculate distance
        di=(findDis(heel,hip))*100
        Label(win,text='Analysis',font=("Times",20),bg='#E6BE09').place(x=740,y=110)
        # Label(win,text=str(int(di)),font=("Times",15)).place(x=850,y=200)
        Label(win,text='Heel to hip '+str(int(di)),font=("Helvetica 18 bold",15),bg="#E6BE09").place(x=740,y=200)
        # Calculate angle
        angle = calculate_angle(rhip, knee, rheel)
        neckangle = calculate_angle(nose, shoulder, elbow)
        if neckangle<100:
            Label(win,text='Senior',font=('Ariel',40),bg="#9AFC04").place(x=750,y=400)
        elif (angle>=140 and angle<=175 and di>=10 and di<=35 ):
            Label(win,text='Injured',font=('Ariel',40),bg="#9AFC04").place(x=750,y=400)
        elif neckangle>110 and di<40:
            Label(win,text='Child',font=('Ariel',40),bg="#9AFC04").place(x=750,y=400)
        elif(neckangle>110 and di>25):
            Label(win,text='Adult',font=('Times',40),bg="#9AFC04").place(x=750, y=400)
        # Visualize angle
        Label(win,text='Neckangle '+str(int(neckangle)),font=("Helvetica 18 bold",15),bg="#E6BE09").place(x=740,y=240)
        # Label(win,text=int(neckangle),font=("Times",15)).place(x=850,y=240)
        Label(win,text='Shoulder angle '+str(int(angle)),font=("Helvetica 18 bold",15),bg="#E6BE09").place(x=740,y=280)
        # Label(win,text=int(angle),font=("Times",15)).place(x=890,y=280)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        Label(win,text='FPS='+str(int(fps)),font=("Helvetica 18 bold",15),bg="#E6BE09").place(x=740,y=320)
        # Render detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #                         mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
        #                         mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
        #                          )  
        # cv2.putText(image , "FPS : ",(40,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
        # cv2.putText(image , str(int(fps)),(160,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
        
        return image
    except:
        return image
######### Main Program ##########
while True:
    _, img = cap.read()
    img = cv2.resize(img, (w, h))
    output=WalkAnalyst(img)
    image = Image.fromarray(output)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    win.update()

