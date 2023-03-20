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
        self.inference_allowed = False
        self.webcamFeed = WebcamFeed(self)

        self.setWindowTitle("My App")
        self.setWindowTitle("Sign Language detector App")
        #self.setContentsMargins(100,100,100,100)
        self.started=False
#                 left,top,width,height
        #   Labels
        self.setGeometry(600, 250, 290, 600)
        # helloMsg = QLabel("<h1>Welcome, User!</h1>", parent=self)
        # helloMsg.move(0, 0)
        layout = QVBoxLayout()

        # self.label = QLabel()
        # pixmap = QPixmap("static\pict_logo.png")
        # self.label.setScaledContents(True)
        # self.label.setPixmap(pixmap)

        #   Current detection, Keywords and sentence label
        self.current_detection_label = QLabel("<b>Currently Detecting</b>", parent=self)
        self.current_detection_label.setStyleSheet(""" 
        *{
            height: fit-content
        }
        """)
        self.detected_keywords_label = QLabel("<b>Detected keywords</b>", parent=self)
        self.detected_keywords_label.setStyleSheet(""" 
        *{
            height: fit-content
        }
        """)
        self.current_detection_placeholder = QLabel("Ready for detection", parent=self)
        self.current_detection_placeholder.setStyleSheet("""
        *{
            background-color: rgb(3, 173, 252);
            border-style: outset;
            border-width: 0px;
            border-radius: 10px;
            color: white;
            font: bold 14px;
            padding: 2px;
            height: fit-content;
        }
        """)
        self.detected_keywords_placeholder = QLabel("Ready for detection", parent=self)
        self.detected_keywords_placeholder.setStyleSheet("""
                *{
                    background-color: rgb(3, 173, 252);
                    border-style: outset;
                    border-width: 0px;
                    border-radius: 10px;
                    color: white;
                    font: bold 14px;
                    padding: 6px;
                    height: fit-content;
                }
            """)
        #   Buttons
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

         #   Add button to confirm sentence
        self.toggle_inference_button = QPushButton("Start signing")
        self.toggle_inference_button.setStyleSheet("""
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
        self.toggle_inference_button.setCheckable(True)
        self.toggle_inference_button.clicked.connect(self.toggle_inference)
        
        # layout.addWidget(self.label)
        layout.addWidget(self.button)        
        layout.addWidget(self.toggle_inference_button)
        layout.addWidget(self.current_detection_label)
        layout.addWidget(self.current_detection_placeholder)
        layout.addWidget(self.detected_keywords_label)
        layout.addWidget(self.detected_keywords_placeholder)
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
        #   TODO:   Call to API for sentence
        #   Reset labels
        self.update_detection_label("Reset for detection")
        self.update_keywords_placeholder("Reset for detection")
        print(keyword_list)

    def toggle_inference(self):
        if not self.inference_allowed:
            self.toggle_inference_button.setText("Stop signing")
        else:
            self.toggle_inference_button.setText("Start signing")
        self.inference_allowed = not self.inference_allowed    
        self.webcamFeed.set_inference_status(allowed=self.inference_allowed)

    def update_detection_label(self, detected_keyword):
        self.current_detection_placeholder.setText("<b>" + detected_keyword + "</b>")

    def update_keywords_placeholder(self, detected_keywords):
        self.detected_keywords_placeholder.setText("<b>" + str(detected_keywords) + "</b>")

#Create an instance of QApplication
app = QApplication(sys.argv)

window = MainWindow()
#Show your application's GUI
window.show()
# window = QWidget()

# Run your application's event loop
sys.exit(app.exec())
