# import pytesseract
# try:
#     from PIL import Image
# except ImportError:
#     import Image
#
# # 列出支持的语言
# print(pytesseract.get_languages(config=''))
#
# print(pytesseract.image_to_string(Image.open(r'.\picture\xiaowangzi1.jpg'), lang='eng'))
from math import *
import numpy as np
import pytesseract
from pytesseract import Output
import cv2
import difflib

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image

def rotate_bound(image, angle:float):    #https://www.jb51.net/article/144471.htm
    '''
     . 旋转图片
     . @param image    opencv读取后的图像
     . @param angle    (逆)旋转角度
    '''

    h, w = image.shape[:2]  # 返回(高,宽,色彩通道数),此处取前两个值返回
    newW = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))
    newH = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    M[0, 2] += (newW - w) / 2
    M[1, 2] += (newH - h) / 2
    return cv2.warpAffine(image, M, (newW, newH), borderValue=(255, 255, 255))



test_shibie = pytesseract.image_to_string(Image.open(r'./test_img/180.jpg'), lang='eng')
# file = open(r"C:\Users\lp896189626\Desktop\project_of_moshishibei\picture\xiaowangzi.txt",
#             'r')  # 打开文件
# text = file.read()  # 读取文件内容

# text1_lines = text.splitlines()
text2_lines = test_shibie.splitlines()

print(text2_lines)

# d = difflib.Differ()
# diff = d.compare(text1_lines, text2_lines)
#
# print("\n".join(list(diff)))

img = cv2.imread(r'./test_img/180.jpg')
# img = rotate_bound(img,180)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

width_list = []
for c in cnts:
    _, _, w, _ = cv2.boundingRect(c)
    width_list.append(w)
wm = np.median(width_list)

tess_text = pytesseract.image_to_data(img, output_type=Output.DICT, lang='eng')
for i in range(len(tess_text['text'])):
    word_len = len(tess_text['text'][i])
    if word_len > 1:
        world_w = int(wm * word_len)
        (x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
        cv2.rectangle(img, (x, y), (x + world_w, y + h), (255, 0, 0), 1)
        im = Image.fromarray(img)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
        draw.text((x, y - 20), tess_text['text'][i], (255, 0, 0), font=font)
        img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

cv2.namedWindow("TextBoundingBoxes", 0)
cv2.imshow("TextBoundingBoxes", img)
cv2.waitKey(0)
