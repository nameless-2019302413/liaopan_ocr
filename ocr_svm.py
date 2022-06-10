import os
from PIL import Image
import urllib
import numpy as np
import cv2
from sklearn.svm import SVC
import joblib
from cutting import *
from svm_training import *


# 进行向量机的训练SVM
def trainSVM():

    array = extractLetters(r'C:\Users\lp896189626\Desktop\ocr_liaopan\temp')
    # 使用向量机SVM进行机器学习
    letterSVM = SVC(kernel="linear", C=1).fit(array[0], array[1])
    return letterSVM


def ocrImg():
    # 传入测试图片，进行识别钡试=def oCrImg(O):
    clf = trainSVM()
    img_path =r'C:\Users\lp896189626\Desktop\ocr_liaopan\picture\xiaowangzi1.jpg'
    position = character_positon(img_path)
    origineImage = cv2.imread(img_path)
    imgs = character(position, origineImage)

    captcha=[]
    for i,img in enumerate(imgs):
        path ='test_img/Letter_%s.png'% i
        im = Image.fromarray(img)
        im.save(path)
        data = getletter(path)
        data = np.array([data])
        oneLetter = clf.predict(data)[0]# print(oneLetter)captcha.append(oneLetter)
        captcha.append(oneLetter)


ocrImg()