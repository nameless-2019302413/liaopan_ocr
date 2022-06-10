import os
from PIL import Image
import numpy as np
import cv2
from sklearn.svm import SVC
import joblib


# 提取SVM用的特征值, 提取字母特征值
def getletter(fn: str):
    fnimg = cv2.imread(fn)  # 读取图像
    img = cv2.resize(fnimg, (10, 18))  # 将图像大小调整为10*18
    alltz = []
    for now_h in range(0, 18):
        xtz = []
        for now_w in range(0, 10):
            b = img[now_h, now_w, 0]
            g = img[now_h, now_w, 1]
            r = img[now_h, now_w, 2]
            btz = 255 - b
            gtz = 255 - g
            rtz = 255 - r
            if btz > 0 or gtz > 0 or rtz > 0:
                nowtz = 1
            else:
                nowtz = 0
            xtz.append(nowtz)
        alltz += xtz
    return alltz


# 提取特征值
def extractLetters(path: str):
    x = []
    y = []
    # 遍历文件夹 获取下面的目录
    for root, sub_dirs, files in os.walk(path):
        for dirs in sub_dirs:
            # 获得每个文件夹的图片
            for fileName in os.listdir(path + '\\' + dirs):
                # print(fileName[0])
                # 打开图片,x为特征值，y为标签注意下啊
                try:
                    x.append(getletter(path + '\\' + dirs + '\\' + fileName))
                    y.append(fileName[0])
                except:
                    print(fileName)
                    continue
    return x, y


# 进行向量机的训练SVM
def trainSVM():

    array = extractLetters(r'C:\Users\lp896189626\Desktop\ocr_by_liaopan\temp')
    # 使用向量机SVM进行机器学习
    letterSVM = SVC(kernel="linear", C=1).fit(array[0], array[1])
    return letterSVM


if __name__ == '__main__':
    trainSVM()
