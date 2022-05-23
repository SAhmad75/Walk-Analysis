import cv2
import mediapipe as mp
import time 
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




mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pTime=0
cTime=0
mpDraw = mp.solutions.drawing_utils
drawing = mpDraw.DrawingSpec(thickness = 1 , circle_radius = 1)
cap = cv2.VideoCapture("D:\Project01\O.mp4")
# cap = cv2.VideoCapture("D:\Project01\Adult_1.mp4")
# type(cv2.imread("D:\Project01\Adult_walking_4.mp4"))
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('original',frame)
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        


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
            cv2.putText(image ,str(di),(180,70),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,0),thickness=2)
            
            # Calculate angle
            angle = calculate_angle(rhip, knee, rheel)
            neckangle = calculate_angle(nose, shoulder, elbow)
            if neckangle<100:
                cv2.putText(image ,'Senior',(10,150),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),thickness=1)
            elif (angle>=140 and angle<=175 and di>=10 and di<=35 ):
                cv2.putText(image ,'Injured',(10,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),thickness=1)
            elif neckangle>110 and di<40:
                cv2.putText(image ,'Child',(10,150),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),thickness=1)
            elif(neckangle>110 and di>25):
                cv2.putText(image ,'Adult',(10,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),thickness=1)
            



            
            # Visualize angle
            cv2.putText(image, str(neckangle), 
                           tuple(np.multiply(shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(knee, [240, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                )


            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )      

            cv2.putText(image , "FPS : ",(40,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
            cv2.putText(image , str(int(fps)),(160,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        except:
            pass

cap.release()
cv2.destroyAllWindows()

