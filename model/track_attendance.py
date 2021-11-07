import cv2,os
import numpy as np
from PIL import Image
import base64
import timeit

class FaceDatasetTrain:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # getting front face trained cascade classifier
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local binary Pattern histogram
        self.students = {"seneen": 2621, "shoa":2622, "zynah":2623}
        self.id_list = list(self.students.values())
        self.name_list = list(self.students.keys())
    def datasetGenerator(self, studentid):
        camstream = cv2.VideoCapture(0)# creates a video capture object
        face_count = 0
        while True: #infinite loop to stop when all frames of video object from videocapture processed
            res, img = camstream.read() #res is the return value and img is the image if videocapture successful -> reads frames
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # gray scale converted
            face = self.detector.detectMultiScale(gray, 1.05, 5)  # 1.05 scale factor -> 5% reduced scaling more accurate
            for (x, y, w, h) in face:  # x, y, w, h rectangles coordinates or corners
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draws rectangle around face
                face_count = face_count + 1  # face count
                cv2.imwrite("model/dataset/student." + studentid + '.' + str(face_count) + ".jpg",
                            gray[y:y + h, x:x + w])  # saves the image according to format into the dataset folder
                cv2.imshow('frame', img)  # show the image frame
            if cv2.waitKey(100) & 0xFF == ord('q'):  # very imp for imshow -> wait for 100 miliseconds to imshow()
                break
            # break if 50 face samples collected
            elif face_count > 50:
                break
        camstream.release()  # release webcam
        cv2.destroyAllWindows()

    def train(self):
        image_paths = [os.path.join("model/dataset/", f) for f in os.listdir("model/dataset/")]  # list of all paths for images
        faces = []
        student_ids = []
        for path in image_paths:  # looping through all the paths from image paths list
            pilimg = Image.open(path).convert('L')  # opening image and converting to gray scale using PIL
            imgnp = np.array(pilimg)  # converts image to np array giving individual pixels values
            id = os.path.split(path)[-1].split(".")[1] # getting student id from path
            face = self.detector.detectMultiScale(imgnp)  # extract the face from image
            for (x, y, w, h) in face:  # cornors of rectangle bounding the face coordinates or values
                faces.append(imgnp[y:y + h, x:x + w])
                student_ids.append(self.students[id])
        self.recognizer.train(faces, np.array(student_ids))
        self.recognizer.save('model/trainer.yml')

    def trackAttendance(self, imgdata):
        start = timeit.default_timer()
        self.recognizer.read('model/trainer.yml')
        imgsrc = base64.b64decode(imgdata)
        filename = 'model/studentimg.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgsrc)
        pilimg = Image.open(filename).convert('L')
        img = np.array(pilimg)
        face = self.detector.detectMultiScale(img, 1.05, 5)
        if len(face) <= 0:
            return None
        for (x, y, w, h) in face:
            user, confidence = self.recognizer.predict(img[y:y + h, x:x + w])
            print(f'{user} Found')
            if confidence > 30:  # if confidence is smaller than 30% [keeping a margin] then student not present
                idx = self.id_list.index(user)
                end = timeit.default_timer()
                finish = end - start
                print(f'time taken: {finish}')
                return self.name_list[idx]
            else:
                return "Unknown"
if __name__=='__main__':
    studentobj = FaceDatasetTrain()
    studentobj.train()