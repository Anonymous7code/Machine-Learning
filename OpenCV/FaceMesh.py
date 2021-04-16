# Importing Libraries
import cv2 as cv
import mediapipe as mp

# Initializing video source
mp_draw = mp.solutions.drawing_utils
mp_face = mp.solutions.face_mesh
drawing_specs = mp_draw.DrawingSpec(thickness=1,circle_radius=1)

video = cv.VideoCapture(1)

with mp_face.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as face_mesh:
    while True:
        ret, frame = video.read()
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        res = face_mesh.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        if res.multi_face_landmarks:
            for face_landmark in res.multi_face_landmarks:
                mp_draw.draw_landmarks(frame,face_landmark,mp_face.FACE_CONNECTIONS,drawing_specs,drawing_specs)
        cv.imshow('Hand Pose', frame)
        k = cv.waitKey(1)

        if k == ord('q'):
            break

video.release()
cv.destroyAllWindows()
