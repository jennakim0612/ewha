import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=2)
mp_drawing=mp.solutions.drawing_utils

compare=[(2,4,17),(5,8,0),(9,12,0),(13,16,0),(17,20,0)]

while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h1=hand_landmarks.landmark
            folding=""
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        for mcp, tip, base in compare:
            tip_dist=(h1[base].x-h1[tip].x)**2+(h1[base].y-h1[tip].y)**2
            mcp_dist=(h1[base].x-h1[mcp].x)**2+(h1[base].y-h1[mcp].y)**2
            folding+="01"[tip_dist>mcp_dist]

        folding+=","

        cv2.putText(
            frame,
            folding,
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,0),
            2

        )
    cv2.imshow('Hand Tracking',frame)

    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()

compare=[(2,4,17),(5,8,0),(9,12,0),(13,16,0),(17,20,0)]

while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h1=hand_landmarks.landmark
            folding=""
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        for mcp, tip, base in compare:
            tip_dist=(h1[base].x-h1[tip].x)**2+(h1[base].y-h1[tip].y)**2
            mcp_dist=(h1[base].x-h1[mcp].x)**2+(h1[base].y-h1[mcp].y)**2
            folding+="01"[tip_dist>mcp_dist]

        folding+=","

        cv2.putText(
            frame,
            folding,
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (50,0,0),
            2

        )
    cv2.imshow('Hand Tracking',frame)

    if cv2.waitKey(1)==27:break
cap.release()
cv2.destroyAllWindows()