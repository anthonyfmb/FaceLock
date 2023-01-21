import tensorflow as tf
import numpy as np
from tensorflow import keras
import os, random
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from pathlib import Path
import shutil
import string
import secrets

def removeIdentifierFile(path):
    for file in os.listdir(path):
        if file.find(".Identifier") != -1:
            os.remove(os.path.join(path, file))

def run():
    box = SignupToolBox(10)
    print("initialized signup")
    box.collect_valid_user_data()
    print("user data collected")
    print(box.create_password(20))
    print("model trained")
    #q.put(box.create_password(20))

class SignupToolBox:
    def __init__(self, img_count):
        self.password = None
        self.model = None
        self.img_count = img_count
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        if "test" in os.listdir("./"):
            shutil.rmtree("test")
        if "train" in os.listdir("./"):
            shutil.rmtree("train")
        if "valid_user" in os.listdir("./"):
            shutil.rmtree("valid_user")

    def create_password(self, password_length):
        letters = string.ascii_letters
        digits = string.digits
        special_characters = string.punctuation
        characters_pool = letters + digits + special_characters
        password = ''
        for i in range(password_length):
            password += ''.join(secrets.choice(characters_pool))
        self.password = password
        return password

    def train(self):
        raw_imposters_folder = "imposters"
        raw_valid_user_folder = "valid_user"
        
        imposter_filenames = random.sample(os.listdir(raw_imposters_folder), self.img_count)
        valid_user_filenames = random.sample(os.listdir(raw_valid_user_folder), self.img_count)

        train_valid_user_folder = "train/valid_user"
        train_imposters_folder = "train/imposters"

        Path(train_valid_user_folder).mkdir(parents=True, exist_ok=True)
        Path(train_imposters_folder).mkdir(parents=True, exist_ok=True)

        test_valid_user_folder = "test/valid_user"
        test_imposters_folder = "test/imposters"

        Path(test_valid_user_folder).mkdir(parents=True, exist_ok=True)
        Path(test_imposters_folder).mkdir(parents=True, exist_ok=True)

        class_training_size = int(self.img_count * 0.9)

        for imposter_filename in imposter_filenames[:class_training_size]:
            shutil.copy(os.path.join(raw_imposters_folder, imposter_filename), os.path.join(train_imposters_folder, imposter_filename))

        for imposter_filename in imposter_filenames[class_training_size:]:
            shutil.copy(os.path.join(raw_imposters_folder, imposter_filename), os.path.join(test_imposters_folder, imposter_filename))


        for valid_user_filename in valid_user_filenames[:class_training_size]:
            shutil.copy(os.path.join(raw_valid_user_folder, valid_user_filename), os.path.join(train_valid_user_folder, valid_user_filename))

        for valid_user_filename in valid_user_filenames[class_training_size:]:
            shutil.copy(os.path.join(raw_valid_user_folder, valid_user_filename), os.path.join(test_valid_user_folder, valid_user_filename))

        removeIdentifierFile(train_imposters_folder)
        removeIdentifierFile(test_imposters_folder)
        removeIdentifierFile(train_valid_user_folder)
        removeIdentifierFile(test_valid_user_folder)

        train = ImageDataGenerator(rescale=1/255)
        test = ImageDataGenerator(rescale=1/255)

        train_dataset = train.flow_from_directory("train",
            target_size=(150,150),
            batch_size = 32,
            class_mode = 'binary')
                                                
        test_dataset = test.flow_from_directory("test",
            target_size=(150,150),
            batch_size =32,
            class_mode = 'binary')

        # CNN
        model = keras.Sequential()
        model.add(keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(150,150,3)))
        model.add(keras.layers.MaxPool2D(2,2))

        model.add(keras.layers.Conv2D(64,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        model.add(keras.layers.Conv2D(128,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        model.add(keras.layers.Conv2D(128,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        model.add(keras.layers.Flatten())

        model.add(keras.layers.Dense(512,activation='relu'))

        model.add(keras.layers.Dense(1,activation='sigmoid'))

        model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

        model.fit_generator(train_dataset,
            steps_per_epoch = 250,
            epochs = 10,
            validation_data = test_dataset
        )

        model.save('classifier')
        self.model = model

    def collect_valid_user_data(self):
        camera = cv2.VideoCapture(0)
        valid_user_dir = "valid_user"
        Path(valid_user_dir).mkdir(parents=True, exist_ok=True)
        cv2.startWindowThread()
        camera.set(3, 640)
        camera.set(4, 480)

        count = 0
        while True:
            read_ok, img = camera.read()
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.face_classifier.detectMultiScale(
                gray_img,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                if count < self.img_count:
                    cv2.imwrite(os.path.join(valid_user_dir, f"{count}.png"), img[y:y+h,x:x+w])
                    count += 1
                else:
                    cv2.destroyAllWindows()
                    return 
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Face Detector', img)
        
        
