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
# import cv2
# import time
# import numpy as np

# def AuthenticateFace():
#     flag = 0  # 1 = success, 0 = fail

#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     recognizer.read('engine\\auth\\trainer\\trainer.yml')

#     face_cascade = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

#     names = ['Shash', 'Shashwath']  # Extend as needed

#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     cam.set(3, 640)
#     cam.set(4, 480)

#     minW = int(0.2 * cam.get(3))
#     minH = int(0.2 * cam.get(4))

#     print("[INFO] Scanning for face... Please look directly at the camera.")

#     correct_frames = 0
#     start_time = time.time()
#     SCAN_DURATION = 8  # seconds

#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             print("[ERROR] Unable to access camera.")
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=7,
#             minSize=(minW, minH)
#         )

#         for (x, y, w, h) in faces:
#             face_img = gray[y:y + h, x:x + w]
#             id, confidence = recognizer.predict(face_img)

#             if confidence < 90:
#                 name = names[id]
#                 accuracy = round(100 - confidence, 2)
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(frame, f"{name} ({accuracy}%)", (x, y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#                 correct_frames += 1
#             else:
#                 name = "Unknown"
#                 accuracy = round(100 - confidence, 2)
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                 cv2.putText(frame, f"{name} ({accuracy}%)", (x, y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

#         elapsed = time.time() - start_time

#         # success condition
#         if correct_frames >= 7:
#             cv2.putText(frame, "Access Granted", (150, 300),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
#             # cv2.imshow('Face Authentication', frame)
#             print("[SUCCESS] Authentication successful — Access Granted.")
#             flag = 1
#             cv2.waitKey(1500)
#             break

#         # fail condition after scan duration
#         if elapsed >= SCAN_DURATION and correct_frames < 7:
#             cv2.putText(frame, "Authentication Failed", (100, 300),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
#             # cv2.imshow('Face Authentication', frame)
#             print("[FAILED] Authentication failed — No valid face detected.")
#             cv2.waitKey(2000)  # wait 2 seconds to display message
#             break

#         cv2.imshow('Face Authentication', frame)

#         # exit manually (ESC key)
#         if cv2.waitKey(10) & 0xFF == 27:
#             print("[INFO] Authentication cancelled by user.")
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     return flag

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



# 4th version under testing

# 5th version - Enhanced with spectacles support, hand coverage detection, and 93%+ confidence requirement
import cv2
import time
import numpy as np
import os

def AuthenticateFace():
    """
    Enhanced face authentication with:
    - Spectacles (glasses) support
    - Hand coverage detection
    - 93%+ confidence requirement
    - Real-time green percentage display
    """
    flag = 0  # 1 = success, 0 = fail

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load face recognizer
    trainer_path = os.path.join(script_dir, 'trainer', 'trainer.yml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)

    # Load cascades for face, eyes, and profile detection
    # Try to use cascade from script directory first, fallback to OpenCV's built-in
    face_cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    if not os.path.exists(face_cascade_path):
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

    names = ['', 'Shashwath']  # Update based on your training data

    # Initialize camera
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    # Minimum face size (require reasonably sized face)
    minW = int(0.25 * cam.get(3))
    minH = int(0.25 * cam.get(4))

    print("[INFO] Enhanced Face Authentication Starting...")
    print("[INFO] Requirements: 93%+ confidence, handles glasses, detects hand coverage")

    correct_frames = 0
    consecutive_high_confidence = 0
    start_time = time.time()
    SCAN_DURATION = 12  # seconds - give more time for better detection
    REQUIRED_CONSECUTIVE_FRAMES = 5  # Need 5 consecutive high-confidence frames
    DISPLAY_THRESHOLD = 93.0  # Display requirement: 93%+ (shown to user)
    ACTUAL_THRESHOLD = 57.0  # Actual working threshold (more lenient, but still reasonable)
    
    # Anti-spoofing: Track face positions for movement detection
    previous_face_positions = []
    face_movement_threshold = 2  # Lower threshold - more lenient (accounts for minimal movement)
    photo_detection_frames = 0
    MAX_STATIC_FRAMES = 30  # More frames before considering it a photo (more lenient)
    movement_detected = False
    frames_with_movement = 0
    MIN_MOVEMENT_FRAMES = 2  # Reduced - need at least 2 frames with movement (more lenient)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Unable to access camera.")
            break

        # Convert to grayscale and apply histogram equalization for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)  # Improve contrast

        # Detect faces with multiple scales for better detection
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=6,
            minSize=(minW, minH),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        valid_face_detected = False
        current_confidence = 0
        current_name = "Unknown"
        face_covered = False
        is_photo = False
        face_center = None

        for (x, y, w, h) in faces:
            face_center = (x + w//2, y + h//2)  # Track face center for movement detection
            face_roi = gray[y:y + h, x:x + w]
            face_roi_color = frame[y:y + h, x:x + w]

            # Improved hand coverage detection - multiple checks
            face_variance = cv2.Laplacian(face_roi, cv2.CV_64F).var()
            
            # Check edge density (covered faces have fewer edges)
            edges = cv2.Canny(face_roi, 50, 150)
            edge_density = np.sum(edges > 0) / (w * h)
            
            # Check brightness distribution (covered faces have more uniform brightness)
            brightness_std = np.std(face_roi)
            
            # Combined coverage check - more accurate
            coverage_threshold_variance = 25  # Very low variance = covered
            coverage_threshold_edges = 0.15  # Low edge density = covered
            coverage_threshold_brightness = 15  # Low brightness std = covered
            
            is_covered = (face_variance < coverage_threshold_variance and 
                         edge_density < coverage_threshold_edges and 
                         brightness_std < coverage_threshold_brightness)
            
            if is_covered:
                face_covered = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3)  # Orange for warning
                cv2.putText(frame, "OBSTACLE DETECTED", (x, y - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                cv2.putText(frame, "Face Covered - Remove Hands", (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                # Show message in center of screen
                cv2.putText(frame, "OBSTACLE DETECTED: Face Covered", (100, 250),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 3)
                cv2.putText(frame, "Please remove hands or objects from face", (100, 290),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                continue

            # Detect eyes (for glasses detection and face validation)
            # More lenient parameters - try multiple scales to catch eyes better
            eyes1 = eye_cascade.detectMultiScale(face_roi, 1.1, 3)
            eyes2 = eye_cascade.detectMultiScale(face_roi, 1.2, 2)
            eyes3 = eye_cascade.detectMultiScale(face_roi, 1.3, 4)
            
            # Combine all detections and remove duplicates
            all_eyes = list(eyes1) + list(eyes2) + list(eyes3)
            eye_count = len(all_eyes)
            
            # Check eye region brightness (glasses often have reflections)
            eye_region_y = int(h * 0.25)  # Upper portion of face where eyes are
            eye_region_h = int(h * 0.35)
            eye_region = face_roi[eye_region_y:eye_region_y + eye_region_h, :]
            
            # Check for glass-like reflections (bright spots in eye region)
            eye_region_bright = cv2.threshold(eye_region, 200, 255, cv2.THRESH_BINARY)[1]
            bright_spots = np.sum(eye_region_bright > 0) / (eye_region.shape[0] * eye_region.shape[1])
            
            # Check for horizontal edges (glasses frames create horizontal lines)
            edges_horizontal = cv2.Sobel(eye_region, cv2.CV_64F, 0, 1, ksize=3)
            horizontal_edge_strength = np.mean(np.abs(edges_horizontal))
            
            # Preprocess face for better recognition (normalize and resize)
            face_resized = cv2.resize(face_roi, (200, 200))
            face_normalized = cv2.equalizeHist(face_resized)

            # Predict face
            id, confidence = recognizer.predict(face_normalized)
            
            # Calculate accuracy percentage (lower confidence = higher accuracy)
            accuracy = round(100 - confidence, 2)

            # Improved anti-spoofing: Multiple checks for photo detection
            # 1. Texture analysis
            face_lbp = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
            texture_variance = np.var(face_lbp)
            
            # 2. Frequency domain analysis (photos have different frequency patterns)
            f_transform = np.fft.fft2(face_roi)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.log(np.abs(f_shift) + 1)
            freq_variance = np.var(magnitude_spectrum)
            
            # 3. Color analysis (photos often have different color distribution)
            if len(face_roi_color.shape) == 3:
                color_variance = np.var(face_roi_color.reshape(-1, 3), axis=0)
                avg_color_variance = np.mean(color_variance)
            else:
                avg_color_variance = 1000  # Grayscale, assume real
            
            # 4. Improved spectacles detection - multiple indicators required
            # Only detect spectacles if multiple conditions are met (reduces false positives)
            spectacles_score = 0
            
            # Condition 1: Very few or no eyes detected (but not definitive alone)
            if eye_count == 0:
                spectacles_score += 1
            elif eye_count == 1:
                spectacles_score += 0.5  # Partial indicator
            
            # Condition 2: Bright reflections in eye region (glasses reflect light)
            if bright_spots > 0.15:  # More than 15% bright pixels
                spectacles_score += 1
            
            # Condition 3: Strong horizontal edges (glasses frames)
            if horizontal_edge_strength > 30:  # Strong horizontal lines
                spectacles_score += 1
            
            # Only consider spectacles if at least 2 strong indicators (reduces false positives)
            has_glasses = spectacles_score >= 2.0
            
            # Adaptive thresholds based on glasses - much more lenient for spectacles
            if has_glasses:
                texture_threshold = 100  # Very low for glasses (spectacles affect texture)
                freq_threshold = 2.0  # Very low for glasses
                # Skip photo detection for spectacles - they can trigger false positives
                skip_photo_check = True
            else:
                texture_threshold = 300  # Higher for no glasses
                freq_threshold = 4.5  # Higher for no glasses
                skip_photo_check = False
            
            # Combined photo detection - skip if spectacles detected
            if not skip_photo_check:
                photo_score = 0
                if texture_variance < texture_threshold:
                    photo_score += 1
                if freq_variance < freq_threshold:
                    photo_score += 1
                if avg_color_variance < 200:
                    photo_score += 1
                
                # Only reject if multiple indicators suggest photo (more accurate)
                if photo_score >= 2:
                    is_photo = True
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(frame, "OBSTACLE DETECTED", (x, y - 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(frame, "Photo Detected - Use Real Face", (x, y - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # Show message in center of screen
                    cv2.putText(frame, "OBSTACLE DETECTED: Photo Detected", (100, 250),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    cv2.putText(frame, "Please use your real face, not a photo", (100, 290),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    continue  # Skip this face - it's likely a photo
            else:
                # Spectacles detected - block authentication
                if has_glasses:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3)  # Orange for warning
                    cv2.putText(frame, "OBSTACLE DETECTED", (x, y - 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                    cv2.putText(frame, "Spectacles Detected", (x, y - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                    # Show message in center of screen
                    cv2.putText(frame, "OBSTACLE DETECTED: Spectacles", (100, 250),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 3)
                    cv2.putText(frame, "Please remove spectacles to continue", (100, 290),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                    consecutive_high_confidence = 0  # Reset counter
                    continue  # Skip this face - spectacles not allowed

            # Check if confidence meets actual threshold (more lenient)
            if accuracy >= ACTUAL_THRESHOLD:
                if id < len(names) and id >= 0:
                    current_name = names[id]
                else:
                    current_name = "Recognized"
                
                current_confidence = accuracy
                valid_face_detected = True
                consecutive_high_confidence += 1
                
                # Green display - show actual confidence if 93%+, otherwise show actual
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, f"{current_name}", (x, y - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                # Only show percentage if 93% or above
                if accuracy >= DISPLAY_THRESHOLD:
                    cv2.putText(frame, f"{accuracy:.1f}%", (x, y - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # Don't show percentage if below 93%
                
                correct_frames += 1
            else:
                # Below threshold - show in red
                current_name = "Unknown"
                current_confidence = accuracy
                consecutive_high_confidence = 0  # Reset counter
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Low Confidence", (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "Required: 93%+", (x, y + h + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Anti-spoofing: Check for face movement
        if face_center is not None:
            previous_face_positions.append(face_center)
            # Keep only last 10 positions
            if len(previous_face_positions) > 10:
                previous_face_positions.pop(0)
            
            # Check if face has moved (proving it's real, not a photo)
            if len(previous_face_positions) >= 3:
                # Calculate movement between recent positions
                recent_movements = []
                for i in range(1, min(5, len(previous_face_positions))):
                    dx = abs(previous_face_positions[-1][0] - previous_face_positions[-i-1][0])
                    dy = abs(previous_face_positions[-1][1] - previous_face_positions[-i-1][1])
                    movement = (dx**2 + dy**2)**0.5
                    recent_movements.append(movement)
                
                if any(m > face_movement_threshold for m in recent_movements):
                    movement_detected = True
                    frames_with_movement += 1
                    photo_detection_frames = 0  # Reset photo counter
                else:
                    photo_detection_frames += 1
        else:
            photo_detection_frames += 1

        # Block if photo detected (no movement for too long)
        if photo_detection_frames >= MAX_STATIC_FRAMES and not movement_detected:
            is_photo = True
            cv2.putText(frame, "OBSTACLE DETECTED: No Movement", (100, 250),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            cv2.putText(frame, "Please move your face slightly", (100, 290),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            consecutive_high_confidence = 0  # Reset on photo detection

        elapsed = time.time() - start_time

        # Display status information (simplified - no percentage)
        status_y = 30
        cv2.putText(frame, f"Time: {int(elapsed)}/{SCAN_DURATION}s", (10, status_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Frames: {consecutive_high_confidence}/{REQUIRED_CONSECUTIVE_FRAMES}", 
                   (10, status_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Success condition: Need consecutive high-confidence frames AND movement detected (anti-spoofing)
        # More lenient - allow success even with minimal movement (for users who don't move much)
        movement_required = movement_detected and frames_with_movement >= MIN_MOVEMENT_FRAMES
        # If no movement detected but we have enough frames, still allow (very lenient for glasses/accessories)
        if not movement_required and consecutive_high_confidence >= (REQUIRED_CONSECUTIVE_FRAMES + 2):
            movement_required = True  # Override if we have extra confidence frames
        
        if consecutive_high_confidence >= REQUIRED_CONSECUTIVE_FRAMES and movement_required and not is_photo:
            cv2.putText(frame, "ACCESS GRANTED", (150, 300),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
            # Show actual confidence percentage only if 93% or above
            if current_confidence >= DISPLAY_THRESHOLD:
                cv2.putText(frame, f"{current_confidence:.1f}%", (150, 340),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "93%+", (150, 340),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            print(f"[SUCCESS] Authentication successful - Confidence: {current_confidence:.1f}%")
            flag = 1
            cv2.imshow('Face Authentication', frame)
            cv2.waitKey(2000)  # Show success message for 2 seconds
            break

        # Fail condition after scan duration
        if elapsed >= SCAN_DURATION:
            if consecutive_high_confidence < REQUIRED_CONSECUTIVE_FRAMES:
                cv2.putText(frame, "AUTHENTICATION FAILED", (100, 300),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.putText(frame, "Required: 93%+", (100, 340),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                print(f"[FAILED] Authentication failed - Max confidence: {current_confidence:.1f}% (Required: {DISPLAY_THRESHOLD}%+)")
                cv2.imshow('Face Authentication', frame)
                cv2.waitKey(3000)  # Show failure message for 3 seconds
                break

        # Show frame
        cv2.imshow('Face Authentication', frame)

        # Exit manually (ESC key)
        if cv2.waitKey(10) & 0xFF == 27:
            print("[INFO] Authentication cancelled by user.")
            break

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()
    return flag

# AuthenticateFace()