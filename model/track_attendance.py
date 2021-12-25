import cv2,os
import numpy as np
from PIL import Image
import base64
import timeit

class FaceDatasetTrain:
    def __init__(self):
        """
        Constructor for defining variables
        """
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # getting front face trained cascade classifier
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local binary Pattern histogram used for facial recognition
        self.students = {"seneen": 2621, "shoa":2622, "zynah":2623}# example list of students used in dataset
        self.id_list = list(self.students.values())
        self.name_list = list(self.students.keys())

    def datasetGenerator(self, studentid):
        """
        Generates 50 grayscale images detecting student's face as a dataset
        :param studentid:student's name
        :return: None
        """
        camstream = cv2.VideoCapture(0) # creates a video capture object
        face_count = 0 #counter for dataset images
        while True: #loop till all frames captured are processed
            ret, img = camstream.read() # img is the frame captured
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # gray scale converted
            face = self.detector.detectMultiScale(gray, 1.05, 5)  # 1.05 scale factor -> 5% reduced scaling more accurate
            for (x, y, w, h) in face:  #coordinates of bounding box detecting face
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draws rectangle around face
                face_count = face_count + 1
                cv2.imwrite("model/dataset/student." + studentid + '.' + str(face_count) + ".jpg",
                            gray[y:y + h, x:x + w])  # saves the image according to a filename format into the dataset folder

                cv2.imshow('frame', img)  # show the image frame
            if cv2.waitKey(100) & 0xFF == ord('q'):  # imp for imshow -> wait for 100 miliseconds to imshow()
                break

            elif face_count >= 50:# break if 50 face samples collected
                break
        camstream.release()
        cv2.destroyAllWindows() #releasing camera and destroying cv window

    def testDatasetGenerator(self, studentid):
        """
        Generates 20 images of student as a test dataset
        :param studentid:student's name
        :return: None
        """
        camstream = cv2.VideoCapture(0) # creates a video capture object
        face_count = 0 #counter for dataset images
        while True:
            ret, img = camstream.read()
            cv2.imwrite("model/test_data/student." + studentid + '.' + str(face_count) + ".jpg", img)  # saving image to test dataset folder
            cv2.imshow('frame', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif face_count >= 20:# break if 20 images
                break
        camstream.release()
        cv2.destroyAllWindows() #releasing camera and destroying cv window

    def train(self):
        """
        Function to train the model on dataset of student images
        :return: None
        """
        image_paths = [os.path.join("model/dataset/", f) for f in os.listdir("model/dataset/")]  # list of all paths for images
        faces = []
        student_ids = []
        for path in image_paths:  # traversing through all dataset images
            pilimg = Image.open(path).convert('L')  # opening image and converting to gray scale using PIL
            imgnp = np.array(pilimg)  # converts image to np array giving individual pixels values
            name = os.path.split(path)[-1].split(".")[1] # getting student name from path
            face = self.detector.detectMultiScale(imgnp)  # extract the face from image
            for (x, y, w, h) in face:  # face bounding box coordinates
                faces.append(imgnp[y:y + h, x:x + w])
                student_ids.append(self.students[name]) #getting corresponding id of student
        self.recognizer.train(faces, np.array(student_ids)) #training list of faces corresponding to student ids
        self.recognizer.save('model/trainer.yml')

    def trackAttendance(self, imgdata):
        """
        Identifying Student from frame
        :param imgdata: base64 of frames from webcam
        :return: student name recognized / None / Unknown
        """
        start = timeit.default_timer() #tracking the time for identifying student
        self.recognizer.read('model/trainer.yml')
        imgsrc = base64.b64decode(imgdata)
        filename = 'model/studentimg.jpg'
        with open(filename, 'wb') as f:
            f.write(imgsrc) #generating an image file from base64
        pilimg = Image.open(filename).convert('L') # opening the generated image in grayscale
        img = np.array(pilimg)
        face = self.detector.detectMultiScale(img, 1.05, 5)
        if len(face) <= 0:
            return None #None : no face detected no student present
        for (x, y, w, h) in face:
            user, confidence = self.recognizer.predict(img[y:y + h, x:x + w])
            print(f'{user} Found')
            if confidence > 30:  # if confidence is smaller than 30% [keeping a margin] then student not present
                idx = self.id_list.index(user) #getting index of id recognized
                end = timeit.default_timer()
                finish = end - start
                print(f'time taken: {finish}')
                return self.name_list[idx] #returning student name
            else:
                return "Unknown" # unknown face detected

    def calcAccuracy(self):
        """
        Function to test the face recognizer on test data to measure accuracy.
        :return: accuracy : float datatype
        """
        image_paths = [os.path.join("model/test_data/", f) for f in os.listdir("model/test_data/")]  # list of all paths for images
        success_count = 0 # count on successfully predicted images
        for path in image_paths:
            student_name = os.path.split(path)[-1].split(".")[1] # getting actual student name
            with open(path, "rb") as img:
                imgdata = base64.b64encode(img.read()) #converting images to base64
                result = self.trackAttendance(imgdata) # predicted student
                if result=="Unknown" or None:
                    continue
                elif result==student_name: #correct result from face recognition
                    success_count = success_count + 1
        n = len(image_paths) # total number of images
        accuracy = success_count/n
        return accuracy




if __name__=='__main__':
    studentobj = FaceDatasetTrain()
    studentobj.train()


