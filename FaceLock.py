from PyQt5.QtWidgets import *
import subprocess
import threading

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
chrome = QPushButton('Launch Chrome')
sign_in = QPushButton('Sign In')
sign_up = QPushButton('Sign Up')
layout.addWidget(chrome)
layout.addWidget(sign_in)
layout.addWidget(sign_up)

def sub():
    subprocess.run(["bash setup_mac.sh"], shell=True)


def on_chrome_clicked():
    t = threading.Thread(target=sub)
    t.daemon = True
    t.start()

chrome.clicked.connect(on_chrome_clicked)
chrome.show()

window.setLayout(layout)
window.show()
app.exec()