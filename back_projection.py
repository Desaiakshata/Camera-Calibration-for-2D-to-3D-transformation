import matplotlib.pyplot as plt
import scipy.linalg as lin
import numpy as np
import cv2

def mouse_right_click():
    #the [x, y] for each right-click event will be stored here
    global right_clicks
    right_clicks = list()
    global count
    count=0
    #this function will be called whenever the mouse is right-clicked
    def mouse_callback(event, x, y, flags, params):
        
        global count
        #right-click event value is 2
        if event == 2:
            count=count+1
            if count==1:
                cv2.destroyAllWindows()
            #store the coordinates of the right-click event as a list
            right_clicks.append([x, y])
    #input image        
    path_image =input("Enter your path to the image : ")
    path_image=str(path_image)
    print(type(path_image))
    #path_image="C:/Users/0003225.jpg"
    img = cv2.imread(path_image,0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return right_clicks


for i in range(0,2):
    #camera intrinsic parameters
    Fx=Fy=2469
    Cx=1228.876620888020
    Cy=1012.976060035710
    K = [[ Fx,        0.,        Cx],
         [   0.,      Fy,        Cy],
         [   0.,      0.,          1.               ]]
    K = np.array(K)
    #camera extrinsic parameters
    R = np.eye(3)
    t = np.array([[0],[0],[0]])
    #projection matrix
    P = K.dot(np.hstack((R,t)))
    list1=mouse_right_click()
    print("pixel values u and v for "+"image "+str(i+1)+" "+str(list1))
    print()
    x = np.array([list1[0][0],list1[0][1],1])
    #calculating the 3D world coordinates 
    X = np.dot(lin.pinv(P),x)
    print("X and Y 3D coordinates for " +"image"+str(i+1))
    print("X= " +str(X[0]))
    print("Y= " +str(X[1]))
    print("-"*55)

    
