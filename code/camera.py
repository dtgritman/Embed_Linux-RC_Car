import numpy as np
import cv2

def nothing(x):
    pass

# Finding percentage of parts
def percentage(x, y):
  return int(100 * float(x)/float(y))


'''
    TODO
    - Migrate find level to a true or false

'''

def find_level(matrix):
    sum_of_matrix = len(matrix) * len(matrix[0])
    color_count = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 255:
                color_count = color_count + 1

    print(percentage(color_count, sum_of_matrix))


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('./object_detection/cascades/frontalface_default.xml')
        self.L = [0, 0, 0]
        self.U = [255, 255, 255]
        #lower_red = np.array([0,184,82])
        #upper_red = np.array([13,255,255])
       

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)


        lower_red = np.array([self.L[0], self.L[1], self.L[2]])
        upper_red = np.array([self.U[0], self.U[1], self.U[2]])
        
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(image, image, mask= mask)

        for (x,y,w,h) in faces:
            center_x = x + int(w/2)
            center_y = y+ int(h/2)

            body_x_start = x - h
            body_y_start = y + h
            
            body_x_end = x + (w*2)
            body_y_end = y +(h*4)

            
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,"(" + str(center_x) + " , " + str(center_y) + ")",(x,y - 10), font, 1, (200,255,155), 2, cv2.LINE_AA)

            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            
            # Body rectangle
            cv2.rectangle(image,(body_x_start, body_y_start), (body_x_end, body_y_end),(255,100,0),  2) 
            
            #find_level(mask[body_x_start:body_x_end, body_y_start:body_y_end])

            cv2.circle(image,(center_x, center_y), 10, (0,255,0), -1)

        image = res  

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()