import sys
from subprocess import call
#Import QApplication and all the required widgets
import webcam_feed
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow,QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setWindowTitle("Sign Language detector App")
        self.setContentsMargins(10,10,10,10)
#                 left,top,width,height
        self.setGeometry(600, 250, 100, 100)
        # helloMsg = QLabel("<h1>Welcome, User!</h1>", parent=self)
        # helloMsg.move(0, 0)

        button = QPushButton("Connect to livefeed!")
        button.setGeometry(150,150,50,50)
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        # button.move()
        # button.move(0,0)
        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        # call(["Python",'C:/Users/kshit/Documents/Final Year Project/desktopApp/sign_language_detection/webcam_feed.py'],shell=True)
        webcam_feed.run_feed()
        print("Connected!")

#Create an instance of QApplication
app = QApplication(sys.argv)

window = MainWindow()
#Show your application's GUI
window.show()
# window = QWidget()


# Run your application's event loop
sys.exit(app.exec())