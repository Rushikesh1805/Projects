

from codecs import register
import tkinter as tk
from tkinter import Message, Text
from tkinter import *
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root1",
    passwd="projectdb",
    database="projectdb"
)

window = tk.Tk()
# helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
# answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry('1280x720')
window.configure(background='white smoke')

window.attributes('-fullscreen', True)
w = 1280
h = 720
my_canvas = Canvas(window, width=w, height=h, bg="white")
my_canvas.pack(pady=0)
img = PhotoImage(file="C:/Users/Rushi/Desktop/finalproject/logo3.png")
my_img = my_canvas.create_image(50, 10, anchor=NW, image=img)
# path = "C:/Users/Rushi/Desktop/finalproject/logo3.png"

# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
# img = ImageTk.PhotoImage(Image.open(path))

# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
# panel = tk.Label(window, image=img)


# panel.pack(side="top", fill="y")

# canvas.create_image(0, 0, image=photo, anchor=tk.NW)

# msg = Message(window, text='Hello, world!')

# Font is a tuple of (font_family, size_in_points, style_modifier_string)
message1 = tk.Label(window, text="KJ College of Engineering And Management Research,Pune.",
                    bg="#eb5e0b", fg="white", width=47, height=2, font=('Nunito', 18, 'bold'))
message1.place(x=420, y=7)

message2 = tk.Label(window, text="Face Recognition Attendance Management System",
                    bg="Green", fg="white", width=43, height=2, font=('PT Serif', 24, ' bold'))

message2.place(x=350, y=80)

lbl = tk.Label(window, text="Enter ID", width=17, height=2,
               fg="white", bg="#048BA8", font=('Roboto Mono', 18, ' bold '))
lbl.place(x=500, y=200)

txt = tk.Entry(window, width=20, bg="gray70",
               fg="red", font=('times', 15, ' bold '))
txt.place(x=850, y=215)

lbl2 = tk.Label(window, text="Enter Name", width=17, fg="white",
                bg="#048BA8", height=2, font=('Roboto Mono', 18, ' bold '))
lbl2.place(x=500, y=300)

txt2 = tk.Entry(window, width=20, bg="gray70",
                fg="red", font=('times', 15, ' bold '))
txt2.place(x=850, y=315)

lbl3 = tk.Label(window, text="Notification: ", width=17, fg="white",
                bg="#048BA8", height=2, font=('Roboto Mono', 18, ' bold'))
lbl3.place(x=500, y=400)

message = tk.Label(window, text="", bg="gray70", fg="red", width=30,
                   height=2, activebackground="gray70", font=('times', 13, ' bold '))
message.place(x=850, y=410)

lbl3 = tk.Label(window, text="Attendance : ", width=17, fg="white",
                bg="#048BA8", height=2, font=('Roboto Mono', 18, ' bold'))
lbl3.place(x=500, y=600)


message2 = tk.Label(window, text="", fg="red", bg="gray70",
                    activeforeground="green", width=30, height=3, font=('times', 15, ' bold '))
message2.place(x=850, y=600)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():

        Id = (txt.get())
        name = (txt2.get())
        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            # harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(
                'C:/Users/Rushi/PycharmProjects/pythonnew21/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
            sampleNum = 0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 5)
                    # incrementing sample number
                    sampleNum = sampleNum+1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("C:/Users/Rushi/Desktop/finalproject/Images/ "+name + "."+Id + '.' +
                                str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                    # display the frame
                    cv2.imshow('frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id + " Name : " + name
            row = [Id, name]
            mycursor = mydb.cursor()
            Insert_data = "INSERT INTO register (Id,name) VALUES (%s, %s)"
            VALUES = (str(Id), str(name))
            mycursor.execute(Insert_data, VALUES)

            mydb.commit()
            # with open('C:/Users/Rushi/Desktop/finalproject/Details/Userdetails.csv', 'a+') as csvFile:
            #    writer = csv.writer(csvFile)
            #    writer.writerow(row)
            #    csvFile.close()
            message.configure(text=res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text=res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text=res)

def TrainImages():
      # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    # harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(
        'C:/Users/Rushi/PycharmProjects/pythonnew21/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    faces, Id = getImagesAndLabels(
        "C:/Users/Rushi/Desktop/finalproject/Images")
    recognizer.train(faces, np.array(Id))
    recognizer.save(
        "C:/Users/Rushi/Desktop/finalproject/Imgtrainer/trainer.yml")
    res = "Image Trained"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
          # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read(
        "C:/Users/Rushi/Desktop/finalproject/Imgtrainer/trainer.yml")
    # harcascadePath = "haarcascade_frontalface_default.xml"
    # faceCascade = cv2.CascadeClassifier(
    # cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier(
        'C:/Users/Rushi/PycharmProjects/pythonnew21/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT Id,name FROM register")
    df = mycursor.fetchall()
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'name']

    # df = pd.read_csv(
    #    "C:/Users/Rushi/Desktop/finalproject/Details/Userdetails.csv")
    # cam = cv2.VideoCapture(0)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    mydb.commit()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 40):
                ts = time.time()
                date_ = datetime.datetime.fromtimestamp(
                    ts).strftime('%Y-%m-%d')
                TimeStamp_ = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                name = df.loc[['Id'] == Id] ['name'].values
                tt = str(Id)+"-"+name
                attendance.loc[len(attendance)] = [Id, name, date_, TimeStamp_]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir(
                    "C:/Users/Rushi/Desktop/finalproject/Unknownimages"))+1
                cv2.imwrite("C:/Users/Rushi/Desktop/finalproject/Unknownimages/Image"+str(noOfFile) +
                            ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 5)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date_ = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    TimeStamp_ = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = TimeStamp_.split(":")

    # fileName="C:/Users/Rushi/Desktop/Face-Recognition-Based-Attendance-System-master/#Face-Recognition-Based-Attendance-System-master/attendance2/_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    # attendance.to_csv(fileName,index=False)
    mycursor = mydb.cursor()
    Insert_data = "INSERT INTO attendance (Id,name,date_,Timestamp_) VALUES (%s, %s, %s, %s)"
    VALUES = (str(Id), str(name), str(date_), str(TimeStamp_))
    mycursor.execute(Insert_data, VALUES)

    mydb.commit()
    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)


# clearButton = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow",
    # width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
# clearButton.place(x=950, y=200)
# clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="red", bg="yellow",
    # width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
# clearButton2.place(x=950, y=300)
takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="white", bg="#048BA8",
                    width=18, height=2, activebackground="Red", font=('Roboto Mono', 15, ' bold '))
takeImg.place(x=450, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="white",
                     bg="#048BA8", width=18, height=2, activebackground="Red", font=('Roboto Mono', 15, ' bold '))
trainImg.place(x=700, y=500)
trackImg = tk.Button(window, text="Take Attendance", command=TrackImages, fg="white",
                     bg="#048BA8", width=18, height=2, activebackground="Red", font=('Roboto Mono', 15, ' bold '))
trackImg.place(x=950, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="white", bg="#F42438",
                       width=15, height=2, activebackground="Red", font=('Roboto Mono', 13, ' bold '))
quitWindow.place(x=730, y=700)


window.mainloop()
