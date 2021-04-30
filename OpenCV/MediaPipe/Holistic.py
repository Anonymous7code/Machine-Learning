import mediapipe as mp
import cv2 as cv

mp_draw = mp.solutions.drawing_utils
mp_holo = mp.solutions.holistic

video = cv.VideoCapture(0)
with mp_holo.Holistic(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
) as holistic:

    while True:
        ret, frame = video.read()

        #Normalizing coz using droidcam which by default outputs rotated image
        # frame = cv.rotate(frame,cv.cv2.ROTATE_90_CLOCKWISE)

        #Changing BGR to RGB as mediapipe uses RGB format
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        res = holistic.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        # Drawing multiple landmarks
        mp_draw.draw_landmarks(
            frame,
            res.face_landmarks,
            mp_holo.FACE_CONNECTIONS,
        )
        mp_draw.draw_landmarks(
            frame,
            res.left_hand_landmarks,
            mp_holo.HAND_CONNECTIONS,
        )
        mp_draw.draw_landmarks(
            frame,
            res.right_hand_landmarks,
            mp_holo.HAND_CONNECTIONS,
        )
        mp_draw.draw_landmarks(
            frame,
            res.pose_landmarks,
            mp_holo.POSE_CONNECTIONS,
        )

        cv.imshow("Pose Estimation", frame)

        k = cv.waitKey(1)
        if k == ord("q"):
            break

video.release()
cv.destroyAllWindows()