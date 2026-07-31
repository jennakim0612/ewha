import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=9)
mp_drawing=mp.solutions.drawing_utils

line_style=mp_drawing.DrawingSpec(
    color=(95,0,255),
    thickness=1
)

cir_style=mp_drawing.DrawingSpec(
    color=(95,0,255),
    thickness=3,
    circle_radius=11
)
while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                cir_style,
                line_style
            )
    cv2.imshow('Hand Tracking',frame)

    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()