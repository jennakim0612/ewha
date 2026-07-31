import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)

mp_face=mp.solutions.face_mesh
mp_drawing=mp.solutions.drawing_utils
face=mp_face.FaceMesh(refine_landmarks=True)

cv2.namedWindow("Face")

while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=face.process(image)
    if results.multi_face_landmarks:
        Im=results.multi_face_landmarks[0]
        mp_drawing.draw_landmarks(
            frame,
            Im,
            mp_face.FACEMESH_TESSELATION
        )
    cv2.imshow('Face',frame)
    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()