import sys
import subprocess
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from multiprocessing import Process, Queue
from signup import run

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

def sub():
    subprocess.run(["bash setup_mac.sh"], shell=True)

def sign_in_process():
    password = subprocess.check_output(["python3 signin.py"], shell=True)

def on_chrome_clicked():
    t = threading.Thread(target=sub)
    t.daemon = True
    t.start()

def on_sign_up_clicked():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    #queue = Queue()
    # p = Process(target=run,args=())
    # p.start()
    # p.join()
    # result = queue.get()
    # print (result)
    # t = threading.Thread(target=sub)
    # t.daemon = True
    # t.start()

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