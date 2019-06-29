import matplotlib.pyplot as plt
import scipy.linalg as lin
import numpy as np
import cv2
import numpy.matlib
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
    #path_image="C:/Users/0003225.jpg"
    img = cv2.imread(path_image,0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return right_clicks


#camera intrinsic parameters
Fx=Fy=2469
Cx=1228.876620888020
Cy=1012.976060035710
K = [[ Fx,        0.,        Cx],
     [   0.,      Fy,        Cy],
     [   0.,      0.,          1.               ]]
K = np.array(K)
#camera extrinsic parameters
R = np.eye(3)                  #Rotation matrix 
t = np.array([[0],[0],[0]])    #translation matrix for 1st image
t1 = np.array([[0],[0],[-5]])  #translation matrix for 2nd image
#projection matrix
P1 = K.dot(np.hstack((R,t)))
P2 = K.dot(np.hstack((R,t1)))

list1=mouse_right_click()
print("pixel values u and v for "+"image "+str(list1))
print()
list2=mouse_right_click()
print("pixel values u and v for "+"image "+str(list2))
print()
#pixel values for 2 images stored as a list
m1 = np.array([list1[0][0],list1[0][1],1])
m2 = np.array([list2[0][0],list2[0][1],1])

#SVD
A =np.array([[m1[0]*P1[2,0] - P1[0,0],m1[0]*P1[2,1] - P1[0,1],m1[0]*P1[2,2] - P1[0,2]],
    [m1[1]*P1[2,0] - P1[1,0],m1[1]*P1[2,1] - P1[1,1],m1[1]*P1[2,2] - P1[1,2]],
    [m2[0]*P2[2,0] - P2[0,0],m2[0]*P2[2,1] - P2[0,1],m2[0]*P2[2,2] - P2[0,2]],
    [m2[1]*P2[2,0] - P2[1,0],m2[1]*P2[2,1] - P2[1,1],m2[1]*P2[2,2] - P2[1,2]]])

b = np.array([[m1[0]*P1[2,3] - P1[0,3]],
    [m1[1]*P1[2,3] - P1[1,3]],
    [m2[0]*P2[2,3] - P2[0,3]],
    [m2[1]*P2[2,3]-P2[1,3]]])

u, s, v = np.linalg.svd(A, full_matrices=True)

B = np.dot(np.transpose(u),b)

y = np.true_divide(B[0:3] ,s[0])

X=np.array([])
X= np.dot(v,y)

X = X/(np.matlib.repmat(X[2,:],3,1))
X = X[0:3, :]
points = np.transpose(X)
print(X)
