# import system module
import sys
import numpy as np
import random
# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2
from ui_main_window import *
class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam_hat)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer_hat)
        self.ui.control_bt_moustach.clicked.connect(self.controlTimer_mustach)
        self.ui.control_bt_pic.clicked.connect(self.controlTimer_takePicture)
        self.ui.pushButton.clicked.connect(self.control_hat_mustach)
        self.hat = cv2.imread('cowboy_hat.png')
        self.mst = cv2.imread('moustache.png')
        self.finalImage = self.hat

    def put_hat(self, hat,fc,x,y,w,h):
            face_width = w
            face_height = h
            hat_width = face_width+1
            hat_height = int(0.40*face_height)+1
            hat = cv2.resize(hat,(hat_width,hat_height))
            for i in range(hat_height):
                for j in range(hat_width):
                    for k in range(3):
                        if hat[i][j][k]<235:
                            fc[y+i-int(0.25*face_height)][x+j][k] = hat[i][j][k]
            return fc
    def put_moustache(self, mst,fc,x,y,w,h):

        face_width = w
        face_height = h

        mst_width = int(face_width*0.4166666)+1
        mst_height = int(face_height*0.142857)+1



        mst = cv2.resize(mst,(mst_width,mst_height))

        for i in range(int(0.62857142857*face_height),int(0.62857142857*face_height)+mst_height):
            for j in range(int(0.29166666666*face_width),int(0.29166666666*face_width)+mst_width):
                for k in range(3):
                    if mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k] <235:
                        fc[y+i][x+j][k] = mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k]

        return fc
    
    def globalViewCam(self,objectName):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        cascPath = "./haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        faces = faceCascade.detectMultiScale(
             image,
             scaleFactor=1.1,
             minNeighbors=5,
        )

        for (x, y, w, h) in faces:
            if(objectName == "hat"):
                image = self.put_hat(self.hat,image,x,y,w,h)
            elif(objectName == "hat and mustache"):
                image = self.put_hat(self.hat,image,x,y,w,h)
                image = self.put_moustache(self.mst,image,x,y,w,h)
            elif(objectName=="mustache"):
                image = self.put_moustache(self.mst,image,x,y,w,h)
        self.finalImage = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)


        anterior = 0

        if anterior != len(faces):
            anterior = len(faces)

        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
    def globalController(self,buttonName):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)
            if(buttonName=="mustache"):
                self.ui.control_bt_moustach.setText("Stop")
            elif(buttonName=="hat"):
                self.ui.control_bt.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            if(buttonName=="mustache"):
                self.ui.control_bt_moustach.setText("Mustache")
            elif(buttonName=="hat"):
                self.ui.control_bt.setText("Hat")

    # view camera
    def viewCam_hat(self):
        self.globalViewCam("hat")

    def viewCam_mustach(self):
        self.globalViewCam("mustache")

    def viewCam_hat_mustach(self):
        self.globalViewCam("hat and mustache")


    def controlTimer_mustach(self):
        self.timer.timeout.connect(self.viewCam_mustach)
        self.globalController("mustache")

    def controlTimer_takePicture(self):
          # if timer is stopped
        if not self.timer.isActive():
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt_pic.setText("Click Again")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # update control_bt text
            cv2.imwrite('images/image'+str(random.randint(0,10000))+'.png',self.finalImage)
            self.ui.control_bt_pic.setText("Capture Image")

    def controlTimer_hat(self):
        self.timer.timeout.connect(self.viewCam_hat)
        self.globalController("hat")

    def control_hat_mustach(self):
        self.timer.timeout.connect(self.viewCam_hat_mustach)
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.pushButton.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.pushButton.setText("Hat And Mustach")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())