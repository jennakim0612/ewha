import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)

mp_face=mp.solutions.face_mesh
face=mp_face.FaceMesh(refine_landmarks=True)
cv2.namedWindow("Face")

width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=face.process(image)

    if results.multi_face_landmarks:
        Im=results.multi_face_landmarks[0]
        eye1=(int(Im.landmark[158].x*width), int(Im.landmark[58].y*height))
        eye2=(int(Im.landmark[153].x*width), int(Im.landmark[153].y*height))

        dist_eye=(eye1[0]-eye2[0])**2+(eye1[1]-eye2[1])**2
        print(dist_eye)

        if (dist_eye>3000): 
            cv2.putText(frame, "^o^", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
        else: 
            cv2.putText(frame,"-_-",(50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

    cv2.imshow('Face',frame)
    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()