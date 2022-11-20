import sys
from subprocess import call
#Import QApplication and all the required widgets
import webcam_feed
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow,QPushButton, QGridLayout
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setWindowTitle("Sign Language detector App")
        #self.setContentsMargins(100,100,100,100)
        self.started=False
#                 left,top,width,height
        self.setGeometry(600, 250, 290, 290)
        # helloMsg = QLabel("<h1>Welcome, User!</h1>", parent=self)
        # helloMsg.move(0, 0)

        self.label = QLabel(self)
        pixmap = QPixmap("static\dhh.png")
        self.label.setPixmap(pixmap)
        self.label.setMinimumWidth(260)
        self.label.setMinimumHeight(260)

        self.button = QPushButton("Connect to livefeed!")
        self.button.setStyleSheet("""
        *{
            height: 30%;
            margin-top: 300%;
            background-color: rgb(128, 60, 224);
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            padding: 6px;
        }
        QPushButton:hover{
            background-color: rgb(193, 81, 241);
        }
        """)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        if not self.started:
            self.started=True
            self.button.setText("Disconnect livefeed")
            webcam_feed.run_feed()
        else:

            self.started=False
            webcam_feed.stop_feed()
            self.button.setText("Connect to livefeed!")
            
        print("Connected!")

#Create an instance of QApplication
app = QApplication(sys.argv)

window = MainWindow()
#Show your application's GUI
window.show()
# window = QWidget()


# Run your application's event loop
sys.exit(app.exec())