import cv2
import time
import numpy as np

#to save the video as output file
fourcc=cv2.VideoWriter_fourcc(*"XVID")
output_file=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

#starting the webcame
cap=cv2.VideoCapture(0)
#allow the webcame to start by making the code sleep for 2 seconds
time.sleep(2)
bg=0

#capturing bg for 60 frames
for i in range(60):
    ret , bg=cap.read()

#flipping the bg
bg=np.flip(bg,axis=1)
#reading the captured frame until the camera is stopped
while(cap.isOpened()):
    ret , img=cap.read()
    if not ret:
        break
    #flipping the image for consistency
    img=np.flip(img,axis=1)
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#generating mask to detect red color
#these values can also be changed as per the color
lower_red=np.array([0,120,50])
upper_red=np.array([10,255,255])
mask_1=cv2.inRange(hsv,lower_red,upper_red)

lower_red=np.array([170,120,70])
upper_red=np.array([180,255,255])
mask_2=cv2.inRange(hsv,lower_red,upper_red)
mask_1=mask_1+mask_2

#open and expand the image where there is mask 1
mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
#create a mask to segment the red color only
mask_2=cv2.bitwise_not(mask_1)

res_1=cv2.bitwise_and(img,img,mask=mask_2)
res_2=cv2.bitwise_and(bg,bg,mask=mask_1)
final_output=cv2.addWeighted(res_1,1,res_2,1,0)
output_file.write(final_output)
cv2.imshow("magic",final_output)
cv2.waitKey(1)
cap.release()
out.release()
cv2.destroyAllWindows()