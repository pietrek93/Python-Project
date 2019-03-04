import cv2
import os
import datetime

from motion import Motion

class Detect:
    gray=0
    img=0
    def __init__(self, image, scale_factor=1.1, min_neighbors=2, facedata="haarcascade_frontalface_default.xml" , min_size=(0,0), max_size=(0,0)):
        self.image = image
        self.facedata = facedata
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.flags = 0
        self.min_size = min_size
        self.max_size = max_size

        #self.counter = 0

    def face_detect(self):
        """
        read xml for training data
        read image file
        get image size
        resize the image
        convert image to grayscale
        load input image in grayscale mode
        use cv2.CascadeClassifier.detectMultiScale() to find faces
        """


        try:

            print(type(self.facedata))
            facedata = "./data/"+self.facedata
            cascade = cv2.CascadeClassifier(facedata)
            Detect.img = cv2.imread(self.image)
            Detect.gray = cv2.cvtColor(Detect.img, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(Detect.gray, self.scale_factor, self.min_neighbors, self.flags, self.min_size, self.max_size)

            return faces
        except cv2.error as e:
            print("cv2.error:", e)
        except Exception as e:
            print("Exception:", e)

    def facecrop(self, faces):
        """
        The face labelled as ROI (region of interest) shows an example of the facial regions that were used in the face analyses.
        Draw a Rectangle around the detected face
        Save the detected face to a jpg file
        """
        try:
            #counter=self.counter
            counter_face=0
            for f in faces:
                counter_face = counter_face + 1
                x, y, w, h = [v for v in f]
                cv2.rectangle(Detect.gray, (x, y), (x + w, y + h), (255, 255, 255),2)
                roi_color = Detect.img[y:y + h, x:x + w]
                fname, ext = os.path.splitext(self.image)
                print(fname, ext)
                fname = fname.split("/")[-1]
                print(fname,ext)
                cv2.imwrite("./faces/" + datetime.date.today().strftime("%d.%m.%y")+ "/" + fname + "_" + "face"+ "_" + str(counter_face) + "_" + datetime.datetime.now().strftime("%H-%M") + ext, roi_color)
            cv2.imwrite("./faces/" + datetime.date.today().strftime("%d.%m.%y")+ "/" + fname + "_" "original" + "_" + datetime.datetime.now().strftime("%H-%M") + ext, Detect.img)

        except cv2.error as e:
            print("cv2.error:", e)
        # except Exception as e:
        #     print("Exception:", e)
        else:
            if (counter_face > 0):
                print("Successfully detected %d face/s" % counter_face)
                #os.remove(self.image)
                return True
            else:
                print("Face not detected")
                #os.remove(self.image)
                return False

