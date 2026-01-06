import cv2
import numpy as np
from PIL import Image #pillow package
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path for samples already taken (relative to script directory)
path = os.path.join(script_dir, 'samples')

# Construct path to cascade file
cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
# If cascade file doesn't exist in script directory, try OpenCV's built-in cascades
if not os.path.exists(cascade_path):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier(cascade_path)
#Haar Cascade classifier is an effective object detection approach


def Images_And_Labels(path): # function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths: # to iterate particular image path

        gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_arr = np.array(gray_img,'uint8') #creating an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Construct path to trainer directory
trainer_dir = os.path.join(script_dir, 'trainer')
os.makedirs(trainer_dir, exist_ok=True)  # Create directory if it doesn't exist
trainer_path = os.path.join(trainer_dir, 'trainer.yml')
recognizer.write(trainer_path)  # Save the trained model as trainer.yml

print("Model trained, Now we can recognize your face.")