import numpy as np
import cv2

def nothing(x):
    pass

# Finding percentage of parts
def percentage(x, y):
  return int(100 * float(x)/float(y))

def find_level(matrix):
    sum_of_matrix = len(matrix) * len(matrix[0])
    color_count = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 255:
                color_count = color_count + 1

    print(percentage(color_count, sum_of_matrix))

# cascades taken from opencv cascades git
face_cascade = cv2.CascadeClassifier('./cascades/frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('./cascades/profileface.xml')

# Window for sliders
#cv2.namedWindow('sliders')

cap = cv2.VideoCapture(0)


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    lower_red = np.array([0,184,82])
    upper_red = np.array([13,255,255])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        center_x = x + int(w/2)
        center_y = y+ int(h/2)

        body_x_start = x - h
        body_y_start = y + h
        
        body_x_end = x + (w*2)
        body_y_end = y +(h*4)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,"(" + str(center_x) + " , " + str(center_y) + ")",(x,y - 10), font, 1, (200,255,155), 2, cv2.LINE_AA)

        # cv2.putText(img,"Threat level: Potato",(x,y - 30), font, 1, (40,0,255), 2, cv2.LINE_AA)
        

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        # Body rectangle
        cv2.rectangle(img,(body_x_start, body_y_start), (body_x_end, body_y_end),(255,100,0),  2) 

        #find_level(mask[body_y_start:body_y_end, body_x_start:body_x_end])

        cv2.circle(img,(center_x, center_y), 10, (0,255,0), -1)
        
        close_up = img[y:y+h, x:x + w]
       # cv2.imshow('face', close_up)
        


    ''' 
        Create a sliders for the slider window
        cv2.createTrackbar("L0", "sliders",0,255,nothing)
        cv2.createTrackbar("L1", "sliders",0,255,nothing)
        cv2.createTrackbar("L2", "sliders",0,255,nothing)

        cv2.createTrackbar("U0", "sliders",0,255,nothing)
        cv2.createTrackbar("U1", "sliders",0,255,nothing)
        cv2.createTrackbar("U2", "sliders",0,255,nothing)


        r = cv2.getTrackbarPos("L0", "sliders")
        g = cv2.getTrackbarPos("L1", "sliders")
        b = cv2.getTrackbarPos("L2", "sliders")


        ur = cv2.getTrackbarPos("U0", "sliders")
        ug = cv2.getTrackbarPos("U2", "sliders")
        ub = cv2.getTrackbarPos("U2", "sliders")
    '''

    #res = cv2.bitwise_and(frame, frame, mask= mask)

    #cv2.imshow('mask',mask)
    # Debuging 
    # cv2.imshow('res',res)
    # cv2.imshow('red', frame)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27 :
        break

cap.release()
cv2.destroyAllWindows()