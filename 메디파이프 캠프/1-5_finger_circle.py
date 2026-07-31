import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=2)
mp_drawing=mp.solutions.drawing_utils

line_style=mp_drawing.DrawingSpec(
    color=(0,0,0),
    thickness=9
)

cir_style=mp_drawing.DrawingSpec(
    color=(255,228,0),
    thickness=3,
    circle_radius=3
)
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks, handness in zip(results.multi_hand_landmarks, results.multi_handedness):
            finger_point=hand_landmarks.landmark[8]
            finger_x=int(finger_point.x*width)
            finger_y=int(finger_point.y*height)

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                cir_style,
                line_style
            )
            cv2.circle(frame,(finger_x,finger_y),30,(218,217,255),10)
            
            handType=handness.classification[0].label
            x=int(hand_landmarks.landmark[0].x*width)
            y=int(hand_landmarks.landmark[0].y*height)

            cv2.putText(
                frame,
                handType,
                (x,y),
                cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                1,
                (0,255,0),
                2
            )
    cv2.imshow('Hand Tracking',frame)

    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()