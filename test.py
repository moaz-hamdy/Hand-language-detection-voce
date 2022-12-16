
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
calssifire = Classifier('model/keras_model.h5', 'model/labels.txt')

offset = 20
imgsize = 300
counter = 0
folder = "data/g"
labels = ['i love you ', 'hello ', 'good', 'yes']

while True:
    success, img = cap.read()
    imgoutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgwhite = np.ones((imgsize, imgsize, 3), np.uint8)*255

        imgcrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

        imgcropshape = imgcrop.shape

        ratio = h/w

        if ratio > 1:
            k = imgsize/h
            wcal = math.ceil(k*w)
            imgresize = cv2.resize(imgcrop, (wcal, imgsize))
            imgresizeshape = imgresize.shape
            wgap =  math.ceil((imgsize-wcal)/2)
            imgwhite[:, wgap :wcal+wgap] = imgresize
            prediction, index = calssifire.getPrediction(imgwhite, draw= False)
            print (prediction, index)

        else:
            k = imgsize / w
            hcal = math.ceil(k * h)
            imgresize = cv2.resize(imgcrop, (imgsize, hcal))
            imgresizeshape = imgresize.shape
            hgap = math.ceil((imgsize - hcal) / 2)
            imgwhite[hgap:hcal + hgap, :] = imgresize
            prediction, index = calssifire.getPrediction(imgwhite, draw= False)



        cv2.putText(imgoutput, labels[index], (x, y-20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)

        if yes == labels[0]:
            text = pyttsx3.init()
            text.say("i love you ")
            text.runAndWait()

        if input_1 == labels[1]:
            text = pyttsx3.init()
            text.say("hello ")
            text.runAndWait()
        if input_1 == labels[2]:
            text = pyttsx3.init()
            text.say("good ")
            text.runAndWait()
        if input_1 == labels[3]:
            text = pyttsx3.init()
            text.say("yes")
            text.runAndWait()

        cv2.imshow('imgcrop', imgcrop)
        cv2.imshow('imgwhite', imgwhite)


    cv2.imshow('image',imgoutput)
    key = cv2.waitKey(1)