import sys
import subprocess
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from multiprocessing import Process, Queue
# from signup import run
from threading import Thread
from time import sleep
from autofiller import AutoFiller

# class WelcomeScreen(QDialog):
#     def __init__(self):
#         super(WelcomeScreen, self).__init__()
#         loadUi("welcomescreen.ui",self)
#         self.login.clicked.connect(self.gotologin)
#         self.create.clicked.connect(self.gotocreate)

#     def gotologin(self):
#         login = LoginScreen()
#         widget.addWidget(login)
#         widget.setCurrentIndex(widget.currentIndex()+1)

#     def gotocreate(self):
#         create = CreateAccScreen()
#         widget.addWidget(create)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
password = ""

def sub():
    subprocess.run(["bash setup_mac.sh"], shell=True)

def sign_in_process():
    password = subprocess.check_output(["python3 signin.py"], shell=True)

def on_chrome_clicked():
    t = threading.Thread(target=sub)
    t.daemon = True
    t.start()

def on_sign_up_clicked():
    output = subprocess.run(["python3", "signup.py"], capture_output=True)
    # stdout_index = output.find("stdout=b'")
    # end_index = output.find("',", stdout_index)
    # stdout_index = (stdout_index + len("stdout=b'"))
    # print(f"test: {output[stdout_index:end_index]}")
    password = output.stdout.decode()

    a = AutoFiller()
    a.send_pass(output.stdout.decode())

def on_sign_in_clicked():
    output = subprocess.run(["python3", "signin.py"], capture_output=True)

    a = AutoFiller()
    a.send_pass(output.stdout.decode())

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
chrome = QPushButton('Launch Chrome')
sign_in = QPushButton('Sign In')
sign_up = QPushButton('Sign Up')

layout.addWidget(chrome)
layout.addWidget(sign_in)
layout.addWidget(sign_up)
# app = QApplication(sys.argv)
# welcome = WelcomeScreen()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(welcome)
# widget.setFixedHeight(800)
# widget.setFixedWidth(1200)
# widget.show()

chrome.clicked.connect(on_chrome_clicked)
sign_up.clicked.connect(on_sign_up_clicked)
chrome.show()

window.setLayout(layout)
window.show()
app.exec()