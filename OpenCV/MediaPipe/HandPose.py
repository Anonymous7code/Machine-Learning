# Importing Libraries
import cv2 as cv
import mediapipe as mp

# Initializing video source
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

video = cv.VideoCapture(0)


with mp_hand.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = video.read()
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        res = hands.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        if res.multi_hand_landmarks:
            for hand_landmark in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS)
        cv.imshow('Hand Pose', frame)
        k = cv.waitKey(1)

        if k == ord('q'):
            break

video.release()
cv.destroyAllWindows()