import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from cutting import *
import os

from PIL import Image

def make_dir():
    for recNum in range(65,91):
        path = 'C:/Users/lp896189626/Desktop/ocr_by_liaopan/temp/' + chr(recNum)
        if not os.path.exists(path):
            os.mkdir(path)

    for recNum in range(45,58):
        path = 'C:/Users/lp896189626/Desktop/ocr_by_liaopan/temp/' + chr(recNum)
        if not os.path.exists(path):
            os.mkdir(path)

    for recNum in range(97, 123):
        path = 'C:/Users/lp896189626/Desktop/ocr_by_liaopan/temp/' + chr(recNum)
        if not os.path.exists(path):
                os.mkdir(path)


# 将切割好的图片，调用tesseract进行识别，然后保存到识别的目录里
def ocrImgAndSave(fileName, imgs):

    for i in range(len(imgs)):
        recNum = pytesseract.image_to_string(imgs[i], lang='eng',config='--psm 10')
        recNum=recNum.replace('\n', '')


        if ( len(recNum) == 1 ):# if (recNum.isalpha() and len(recNum) == 1)
            # print('zhenzaizhix')
            # recNum = pytesseract.image_to_string(cur_img, config='-psm 10 outputbase digits')

            if((ord(recNum) in range(65,91)) or (ord(recNum) in range(97,123)) or (ord(recNum) in range(45,58))):
                recdString = fileName + "__" + str(i + 1) + ".png"

                path = '//temp1/'
                imgPath = path +'/'+recNum+'/'+ recdString
                im = Image.fromarray(imgs[i])
                im.save(imgPath)

if __name__=="__main__":
    make_dir()
    for i in range(6,7):
        img_path= r'./training_img/' + str(i) +r'.png'
        print('正在处理第' + str(i) + '张图片')
        origineImage = cv2.imread(img_path)
        position = character_positon(img_path)
        img_character = character(position, origineImage)
        ocrImgAndSave(str(i),img_character)