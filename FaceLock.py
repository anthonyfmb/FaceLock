import sys
import subprocess
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from multiprocessing import Process, Queue
from threading import Thread
from time import sleep
from os import wait
from autofiller import AutoFiller
import requests
import socket

db_url = "http://localhost:8000/customers/"

def sub():
    subprocess.run(["bash setup_mac.sh"], shell=True)

def on_chrome_clicked():
    t = threading.Thread(target=sub)
    t.daemon = True
    t.start()
    chrome_opened = True

class WelcomeScreen(QDialog):
    def __init__(self):
        chrome_opened = False
        super(WelcomeScreen, self).__init__()
        #loadUi("welcomescreen.ui",self)
        # self.login.clicked.connect(self.on_sign_in_clicked)
        # self.create.clicked.connect(self.on_sign_up_clicked)
        # self.chrome.clicked.connect(on_chrome_clicked)
        self.password = ""
        self.signed_up = False
    
    def beginWait(self):
        chrome.deleteLater()
        sign_in.deleteLater()
        sign_up.deleteLater()
        label = QLabel()
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText("first line\nsecond line")
        layout.addWidget(label)

    def on_sign_up_clicked(self):
        output = subprocess.run(["python3", "signup.py"], capture_output=True)
        self.password = output.stdout.decode()
        print("PASS: " + self.password)
        self.signed_up = True

    def on_sign_in_clicked(self):
        output = subprocess.run(["python3", "signin.py"], capture_output=True)

        print(output.stdout.decode())
        if (output.stdout.decode() == '1\n'):
            a = AutoFiller()
            hostname = socket.gethostname()   
            ip = socket.gethostbyname(hostname)
            query = {"name": ip}
            db_password = requests.get(db_url, json = query)
            print("PASS SIGN IN:" + db_password)
            a.send_pass(db_password)
        else:
            print("bruh")

# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()
# chrome = QPushButton('Launch Chrome')
# sign_in = QPushButton('Sign In')
# sign_up = QPushButton('Sign Up')

# layout.addWidget(chrome)
# layout.addWidget(sign_in)
# layout.addWidget(sign_up)

# app = QApplication(sys.argv)
# welcome = WelcomeScreen()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(welcome)
# widget.setFixedHeight(250)
# widget.setFixedWidth(250)
# widget.show()

# chrome.clicked.connect(on_chrome_clicked)
# sign_up.clicked.connect(on_sign_up_clicked)
# chrome.show()

# window.setLayout(layout)
# window.show()
app = QApplication([])
welcome = WelcomeScreen()

window = QWidget()
layout = QVBoxLayout()
chrome = QPushButton('Launch Chrome')
sign_in = QPushButton('Sign In')
sign_up = QPushButton('Sign Up')

layout.addWidget(chrome)
layout.addWidget(sign_in)
layout.addWidget(sign_up)
chrome.clicked.connect(on_chrome_clicked)
sign_in.clicked.connect(welcome.on_sign_in_clicked)
sign_up.clicked.connect(welcome.on_sign_up_clicked)
chrome.show()

window.setLayout(layout)
window.show()
app.exec()