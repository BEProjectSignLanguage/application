import sys
from subprocess import call
#Import QApplication and all the required widgets
from webcam_feed import WebcamFeed
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt6.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.webcamFeed = WebcamFeed()

        self.setWindowTitle("My App")
        self.setWindowTitle("Sign Language detector App")
        #self.setContentsMargins(100,100,100,100)
        self.started=False
#                 left,top,width,height
        self.setGeometry(600, 250, 290, 290)
        # helloMsg = QLabel("<h1>Welcome, User!</h1>", parent=self)
        # helloMsg.move(0, 0)
        layout = QVBoxLayout()

        self.label = QLabel()
        pixmap = QPixmap("static\pict_logo.png")
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

        self.button = QPushButton("Connect to livefeed!")
        self.button.setStyleSheet("""
        *{
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
        self.button.clicked.connect(self.toggle_feed)

        #   Add button to confirm sentence
        self.confirm_button = QPushButton("Confirm sentence")
        self.confirm_button.setStyleSheet("""
        *{
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
        self.confirm_button.setCheckable(True)
        self.confirm_button.clicked.connect(self.confirm_sentence)
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

    def toggle_feed(self):
        if not self.started:
            self.started=True
            self.button.setText("Disconnect livefeed")
            self.webcamFeed.run_feed()
            print("Connected!")
        else:
            self.started=False
            self.webcamFeed.stop_feed()
            self.button.setText("Connect to livefeed!")            
            print("Disconnected!")

    def confirm_sentence(self):
        keyword_list = self.webcamFeed.keywords
        self.webcamFeed.reset_occurence_counter()
        self.webcamFeed.keywords = []
        print(keyword_list)

#Create an instance of QApplication
app = QApplication(sys.argv)

window = MainWindow()
#Show your application's GUI
window.show()
# window = QWidget()

# Run your application's event loop
sys.exit(app.exec())
