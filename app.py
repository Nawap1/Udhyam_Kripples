import os
from deepface import DeepFace
import cv2

def check_and_remove_duplicates(input_image_path):
    '''
    Takes an image path as input and checks with each image in the directory then if it matches with any image 
    then it returns True and removes matched image else returns False 
    '''
    dirs = os.listdir('./images/')
    for i in ['./images/'+ files for files in dirs]:
        result = DeepFace.verify(input_image_path,i)['verified']
        if result:
            print('Found')
            os.remove(i)# Removes the found image to save space
            return
    print('Not Found')
    
def click_photo_enter():
    """
    Takes photo from camera using opencv after clicking enter key and save it under image.png 
    """
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read() # return a single frame in variable `frame`

    while(True):
        cv2.imshow('img1',frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
            num = len(os.listdir('./images/'))
            cv2.imwrite(f'images/{num}.jpg',frame) #saves the image in images directory
            cv2.destroyAllWindows()
            break

    cap.release()
    
def click_photo_exit():
    """
    Takes photo from camera using opencv after clicking enter key and save it under image.png 
    """
    import cv2

    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read() # return a single frame in variable `frame`

    while(True):
        cv2.imshow('img1',frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
            cv2.imwrite('test.jpg',frame)
            cv2.destroyAllWindows()
            break

    cap.release()
    return 'test.jpg'

click_photo_enter()#clicks and saves image in images directory while entering
image_path = click_photo_exit()# clicks and saves image in images directory while exiting
check_and_remove_duplicates(image_path)# checks and removes duplicates in images directory