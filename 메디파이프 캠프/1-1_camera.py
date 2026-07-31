import cv2

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)

while True:
    ret, frame=cap.read()
    if not ret : break

    frame=cv2.flip(frame,1)
    cv2.imshow('Hand Tracking',frame)

    if cv2.waitKey(1)==27:break

cap.release()
cv2.destroyAllWindows()