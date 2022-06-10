import cv2
import numpy as np
import pytesseract
from pytesseract import Output
'''水平投影'''
from aip import AipOcr
import difflib
from PIL import Image
import io

# 定义常量
APP_ID = '26357978'
API_KEY = '5sRlxKmDppHLTkxZoxnZ2riH'
SECRET_KEY = 'GVxHWheI00GtZI8cYyP28nQ7v8bMROXn'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口



def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    (h, w) = image.shape

    # 长度与图像高度一致的数组
    h_ = [0] * h

    # 循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    # cv2.imshow('hProjection2', hProjection)
    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8);
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像宽度一致的数组
    w_ = [0] * w
    # 循环统计每一列白色像素的个数
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1

    # 绘制垂直平投影图像
    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255
    # cv2.imshow('vProjection',vProjection)
    return w_


def character_positon(Imagepath: str):
    # 图像灰度化
    origineImage = cv2.imread(Imagepath)
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', image)

    # 将图片二值化
    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('binary', img)

    # 图像高与宽
    (h, w) = img.shape
    Position = []
    # 水平投影
    H = getHProjection(img)
    start = 0
    H_Start = []
    H_End = []
    # 根据水平投影获取垂直分割位置
    for i in range(len(H)):

        if H[i] > 0 and start == 0:
            H_Start.append(i)
            start = 1

        if H[i] <= 0 and start == 1:
            H_End.append(i)
            start = 0

    # 分割行，分割之后再进行列分割并保存分割位置
    for i in range(len(H_Start)):
        # 获取行图像
        cropImg = img[H_Start[i]:H_End[i], 0:w]
        # cv2.imshow('cropImg',cropImg)
        # 对行图像进行垂直投影
        W = getVProjection(cropImg)
        Wstart = 0
        Wend = 0
        W_Start = 0
        W_End = 0
        for j in range(len(W)):
            if W[j] > 0 and Wstart == 0:
                W_Start = j
                Wstart = 1
                Wend = 0

            if W[j] <= 0 and Wstart == 1:
                W_End = j
                Wstart = 0
                Wend = 1

            if Wend == 1:
                Position.append([W_Start, H_Start[i], W_End, H_End[i]])
                Wend = 0

    # 根据确定的位置分割字符

    return Position


def character(position: list, img):
    img_character=[]
    for m in range(len(position)):
        row_start = position[m][0]
        row_end = position[m][2]
        col_start = position[m][1]
        col_end = position[m][3]
        #print(row_start, row_end, col_start, col_end)
        # cv2图片： [高， 宽]
        child_img = img[col_start:col_end, row_start:row_end]
        # child_img = img[position[m][0]: position[m][1], position[m][2]: position[m][3]]

        img_character.insert(m, child_img)

    return img_character

def ndarray2bytes(img_arr):
    """ndarray的图片转换成bytes"""
    imgByteArr = io.BytesIO()
    Image.fromarray(img_arr).save(imgByteArr, format='PNG')
    img_data = imgByteArr.getvalue()
    return img_data

if __name__ == "__main__":
    # 读入原始图像
    img_path = r'./picture/xiaowangzi1.jpg'
    position = character_positon(img_path)
    origineImage = cv2.imread(img_path)
    img_character_origin = character(position, origineImage)
    img_character=img_character_origin

    # for i in range(10):
    #     cv2.namedWindow("image", 0);
    #     cv2.imshow('image', img_character[i])

    for m in range(len(position)):
        cv2.rectangle(origineImage, (position[m][0], position[m][1]), (position[m][2], position[m][3]), (0, 229, 238),
                    1)

   # cv2.namedWindow("image", 0);

    cv2.imshow('image', origineImage)


        #basicGeneral(ndarray2bytes(img_character[36]), options)

    cv2.waitKey(0)
