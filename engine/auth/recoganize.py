# from sys import flags
# import time
# import cv2
# import pyautogui as p


# def AuthenticateFace():

#     flag = ""
#     # Local Binary Patterns Histograms
#     recognizer = cv2.face.LBPHFaceRecognizer_create()

#     recognizer.read('engine\\auth\\trainer\\trainer.yml')  # load trained model
#     cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
#     # initializing haar cascade for object detection approach
#     faceCascade = cv2.CascadeClassifier(cascadePath)

#     font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type


#     id = 2  # number of persons you want to Recognize


#     names = ['', 'Shashwath']  # names, leave first empty bcz counter starts from 0


#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
#     cam.set(3, 640)  # set video FrameWidht
#     cam.set(4, 480)  # set video FrameHeight

#     # Define min window size to be recognized as a face
#     minW = 0.1*cam.get(3)
#     minH = 0.1*cam.get(4)

#     # flag = True

#     while True:

#         ret, img = cam.read()  # read the frames using the above created object

#         # The function converts an input image from one color space to another
#         converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         faces = faceCascade.detectMultiScale(
#             converted_image,
#             scaleFactor=1.2,
#             minNeighbors=5,
#             minSize=(int(minW), int(minH)),
#         )

#         for(x, y, w, h) in faces:

#             # used to draw a rectangle on any image
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

#             # to predict on every single image
#             id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])

#             # Check if accuracy is less them 100 ==> "0" is perfect match
#             if (accuracy < 100):
#                 id = names[id]
#                 accuracy = "  {0}%".format(round(100 - accuracy))
#                 flag = 1
#             else:
#                 id = "unknown"
#                 accuracy = "  {0}%".format(round(100 - accuracy))
#                 flag = 0

#             cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
#             cv2.putText(img, str(accuracy), (x+5, y+h-5),
#                         font, 1, (255, 255, 0), 1)

#         cv2.imshow('camera', img)

#         k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
#         if k == 27:
#             break
#         if flag == 1:
#             break
            

#     # Do a bit of cleanup
    
#     cam.release()
#     cv2.destroyAllWindows()
#     return flag



# newer version under testing
import cv2
import time
import numpy as np

def AuthenticateFace():
    flag = 0  # 1 = success, 0 = fail

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('engine\\auth\\trainer\\trainer.yml')

    face_cascade = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

    names = ['', 'Shashwath', 'User2']  # Extend as needed

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = int(0.2 * cam.get(3))
    minH = int(0.2 * cam.get(4))

    print("[INFO] Scanning for face... Please look directly at the camera.")

    correct_frames = 0
    start_time = time.time()
    SCAN_DURATION = 8  # seconds

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Unable to access camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(minW, minH)
        )

        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            id, confidence = recognizer.predict(face_img)

            if confidence < 60:
                name = names[id]
                accuracy = round(100 - confidence, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} ({accuracy}%)", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                correct_frames += 1
            else:
                name = "Unknown"
                accuracy = round(100 - confidence, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, f"{name} ({accuracy}%)", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        elapsed = time.time() - start_time

        # success condition
        if correct_frames >= 7:
            cv2.putText(frame, "Access Granted", (150, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
            # cv2.imshow('Face Authentication', frame)
            print("[SUCCESS] Authentication successful — Access Granted.")
            flag = 1
            cv2.waitKey(1500)
            break

        # fail condition after scan duration
        if elapsed >= SCAN_DURATION and correct_frames < 7:
            cv2.putText(frame, "Authentication Failed", (100, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            # cv2.imshow('Face Authentication', frame)
            print("[FAILED] Authentication failed — No valid face detected.")
            cv2.waitKey(2000)  # wait 2 seconds to display message
            break

        cv2.imshow('Face Authentication', frame)

        # exit manually (ESC key)
        if cv2.waitKey(10) & 0xFF == 27:
            print("[INFO] Authentication cancelled by user.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag

# AuthenticateFace()



#3rd version under testing
# import cv2
# import time
# import numpy as np

# def AuthenticateFace():
#     flag = 0  # 1 = success, 0 = fail

#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     recognizer.read('engine\\auth\\trainer\\trainer.yml')

#     face_cascade = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#     names = ['', 'Shashwath', 'User2']  # Extend as needed

#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     cam.set(3, 640)
#     cam.set(4, 480)

#     minW = int(0.3 * cam.get(3))  # require bigger visible face
#     minH = int(0.3 * cam.get(4))

#     print("[INFO] Scanning for face... Please look directly at the camera.")

#     correct_frames = 0
#     start_time = time.time()
#     SCAN_DURATION = 10  # seconds

#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             print("[ERROR] Unable to access camera.")
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=8,
#             minSize=(minW, minH)
#         )

#         valid_face_detected = False

#         for (x, y, w, h) in faces:
#             face_img = gray[y:y + h, x:x + w]

#             # Check for both eyes — ensures full visible face
#             eyes = eye_cascade.detectMultiScale(face_img, 1.2, 5)
#             if len(eyes) < 2:
#                 cv2.putText(frame, "Face not fully visible", (100, 400),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
#                 continue  # skip recognition if eyes not visible

#             id, confidence = recognizer.predict(face_img)

#             # Confidence check — very strict
#             if confidence < 50:
#                 accuracy = int(100 - confidence * 0.2)
#                 if accuracy >= 90:  # require very high accuracy
#                     name = names[id]
#                     color = (0, 255, 0)
#                     correct_frames += 1
#                     valid_face_detected = True
#                 else:
#                     name = "Unknown"
#                     color = (0, 0, 255)
#             else:
#                 name = "Unknown"
#                 accuracy = int(max(0, 100 - confidence))
#                 color = (0, 0, 255)

#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, f"{name} ({accuracy}%)", (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

#         elapsed = time.time() - start_time

#         # Success only if multiple strong matches with both eyes visible
#         if correct_frames >= 7 and valid_face_detected:
#             cv2.putText(frame, "Access Granted", (150, 300),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
#             print("[SUCCESS] Authentication successful — Access Granted.")
#             flag = 1
#             cv2.imshow('Face Authentication', frame)
#             cv2.waitKey(1500)
#             break

#         if elapsed >= SCAN_DURATION and correct_frames < 7:
#             cv2.putText(frame, "Authentication Failed", (100, 300),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
#             print("[FAILED] Authentication failed — Face not fully visible or not recognized.")
#             cv2.imshow('Face Authentication', frame)
#             cv2.waitKey(2000)
#             break

#         cv2.imshow('Face Authentication', frame)

#         if cv2.waitKey(10) & 0xFF == 27:
#             print("[INFO] Authentication cancelled by user.")
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     return flag

# AuthenticateFace()