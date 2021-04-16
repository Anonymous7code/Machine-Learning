# Importing Libraries
import cv2 as cv
import mediapipe as mp

# Initializing video source
mp_draw = mp.solutions.drawing_utils
mp_face = mp.solutions.face_mesh
drawing_specs = mp_draw.DrawingSpec(thickness=1,circle_radius=1)

mp_hand = mp.solutions.hands

video = cv.VideoCapture(0)


with mp_face.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as face_mesh:
    with mp_hand.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:

        while True:
            ret, frame = video.read()
            frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            frame.flags.writeable = False
            face_res = face_mesh.process(frame)
            hand_res = hands.process(frame)
            frame.flags.writeable = True
            frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
            if face_res.multi_face_landmarks :
                
                for face_landmark in face_res.multi_face_landmarks:
                    mp_draw.draw_landmarks(frame,face_landmark,mp_face.FACE_CONNECTIONS,drawing_specs,drawing_specs)
            if hand_res.multi_hand_landmarks:
                
                for hand_landmark in hand_res.multi_hand_landmarks:
                    
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS)
            cv.imshow('Hand and Face Pose', frame)
            k = cv.waitKey(1)

            if k == ord('q'):
                break

        

video.release()
cv.destroyAllWindows()


