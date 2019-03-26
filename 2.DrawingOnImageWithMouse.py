import numpy as np
import cv2 

# Making The Blank Image
image = np.zeros((512,512,3))
drawing = False
ix = 0
iy = 0
# Adding Function Attached To Mouse Callback
def draw(event,x,y,flags,params):
    global ix,iy,drawing
    # Left Mouse Button Down Pressed
    if(event==1):
        drawing = True
        ix = x
        iy = y
    if(event==0):
        if(drawing==True):
            cv2.rectangle(image,pt1=(ix,iy),pt2=(x,y),color=(255,255,255),thickness=-1)
    if(event==4):
        drawing = False



# Making Window For The Image
cv2.namedWindow("Window")

# Adding Mouse CallBack Event
cv2.setMouseCallback("Window",draw)

# Starting The Loop So Image Can Be Shown
while(True):

    cv2.imshow("Window",image)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
