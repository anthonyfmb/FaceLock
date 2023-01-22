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
import socket
import requests

font = cv2.FONT_HERSHEY_SIMPLEX

def removeIdentifierFile(path):
    for file in os.listdir(path):
        if file.find(".Identifier") != -1:
            os.remove(os.path.join(path, file))

def predictImage(filename, model):
    img1 = image.load_img(filename,target_size=(150,150)) 
    Y = image.img_to_array(img1)
    X = np.expand_dims(Y,axis=0)
    val = model.predict(X, verbose=0)
    return val[0][0]

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
        
        url = 'http://localhost:8000/customers/'
        hostname = socket.gethostname()   
        ip = socket.gethostbyname(hostname)

        data = {'name': ip, 'password': password}
        resp = requests.post(url, json = data)
        resp = resp.content.decode()
        id_i = resp.find("id")
        end_i = resp.find(",", id_i)
        id = resp[id_i + 4:end_i]

        f = open("id.txt", "w")
        f.write(id)
        f.close()
        return password

    def train(self):
        batch_size = 32

        raw_imposters_folder = "imposters"
        raw_valid_user_folder = "valid_user"
        
        imposter_filenames = random.sample(os.listdir(raw_imposters_folder), self.img_count)
        valid_user_filenames = random.sample(os.listdir(raw_valid_user_folder), self.img_count)

        train_valid_user_folder = "./train/valid_user"
        train_imposters_folder = "./train/imposters"

        Path(train_valid_user_folder).mkdir(parents=True, exist_ok=True)
        Path(train_imposters_folder).mkdir(parents=True, exist_ok=True)

        test_valid_user_folder = "./test/valid_user"
        test_imposters_folder = "./test/imposters"

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

        # removeIdentifierFile(train_imposters_folder)
        # removeIdentifierFile(test_imposters_folder)
        # removeIdentifierFile(train_valid_user_folder)
        # removeIdentifierFile(test_valid_user_folder)

        train = ImageDataGenerator(rescale=1/255)
        test = ImageDataGenerator(rescale=1/255)

        train_dataset = train.flow_from_directory("train",
            target_size=(150,150),
            batch_size = batch_size,
            class_mode = 'binary')
                                                
        test_dataset = test.flow_from_directory("test",
            target_size=(150,150),
            batch_size = batch_size,
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
            steps_per_epoch = train_dataset.samples // batch_size,
            epochs = 5,
            validation_data = test_dataset
        )

        model.save('classifier')
        self.model = model

    def test(self):
        test_imposter = "test/imposters"
        test_valid_user = "test/valid_user"
        correct_count = 0
        wrong_count = 0
        count = 0

        for file in os.listdir(test_imposter):
            id = predictImage(os.path.join(test_imposter, file), self.model)
            count += 1
            if id == 0:
                correct_count += 1
                print(f"{file} correct {id}")
            else:
                wrong_count += 1
                print(f"{file} wrong {id}")


        for file in os.listdir(test_valid_user):
            id = predictImage(os.path.join(test_valid_user, file), self.model)
            count += 1
            if id == 1:
                correct_count += 1
                print(f"{file} correct {id}")
            else:
                wrong_count += 1
                print(f"{file} wrong {id}")
        return (correct_count / count)

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
                    camera.release()
                    break
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    img, 
                    f"{count} / {self.img_count}", 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                )
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

# def run():
box = SignupToolBox(500)
# print("initialized signup")
box.collect_valid_user_data()
# box.train()
box.train()
print(box.test())
# print("user data collected")
print(box.create_password(20))
# print("model trained")
#q.put(box.create_password(20))