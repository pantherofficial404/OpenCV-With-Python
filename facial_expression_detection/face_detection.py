import cv2
import sys
cap = cv2.VideoCapture(0)
from keras.models import load_model
model = load_model('fer2013.h5')

labels = {0:"Angry",1:"Disgust",2:"Fear",3:"Happy",4:"Sad",5:"Surprise",6:"Neutral"}
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

while(True):
    ret,image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(1,1),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Detected Faces",len(faces))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        saveImage = gray[y:y+h,x:x+w]
        saveImage = cv2.resize(saveImage,(48,48))
        result = model.predict_classes(saveImage.reshape(1,48,48,1))[0]
        cv2.putText(image,labels.get(result),(x,y),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=2,color=(0,0,255),thickness=1)
    cv2.imshow("Faces Detected", image)
    if cv2.waitKey(35) == ord('q'):
        break
