import cv2
import numpy as np
import os 
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

class SigninToolBox:
  def __init__(self, model_dir):
    self.model = tf.keras.models.load_model(model_dir)
    self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

  def signin(self):
    camera = cv2.VideoCapture(0)
    cv2.startWindowThread()
    camera.set(3, 640)
    camera.set(4, 480)

    minWeight = 0.1*camera.get(3)
    minHeight = 0.1*camera.get(4)

    user = 0

    while True:
      record_ok, img = camera.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
      faces = self.faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minWeight), int(minHeight)),
      )

      for(x,y,w,h) in faces:
        face = cv2.resize(img[y:y+h,x:x+w], dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
        face_img = Image.fromarray(face, 'RGB')
        Y = image.img_to_array(face_img)
        X = np.expand_dims(Y, axis=0)
        id = self.model.predict(X, verbose = 0)
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        if (id == 1):
          camera.release()
          user = 1
          break
      else:
        cv2.imshow('Face Detector', img)
        if cv2.waitKey(1) & 0xFF == ord('x'):
          break
        continue
      break

    camera.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return user


box = SigninToolBox("classifier")
print(box.signin())