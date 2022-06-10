from aip import AipOcr
import difflib

# 定义常量
APP_ID = '26357978'
API_KEY = '5sRlxKmDppHLTkxZoxnZ2riH'
SECRET_KEY = 'GVxHWheI00GtZI8cYyP28nQ7v8bMROXn'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = r'./test_img/180.jpg'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
print(type(get_file_content(filePath)))
# result = aipOcr.basicGeneral(get_file_content(filePath), options)
test_shibie = ''
# print(result)
words_result = result['words_result']
for i in range(len(words_result)):
    print(words_result[i]['words'])
    test_shibie += words_result[i]['words'] + ' '



# # 对比
# file = open(r"C:\Users\lp896189636\Desktop\project_of_moshishibei\character_recognition\picture\xiaowangzi1.txt",
#             'r')  # 打开文件
# text = file.read()  # 读取文件内容
#
# text1_lines = text.splitlines()
# text2_lines = test_shibie.splitlines()
#
# d = difflib.Differ()
# diff = d.compare(text1_lines, text2_lines)
#
# # print(text1_lines)
# # print(text2_lines)
#
# print("\n".join(list(diff)))
