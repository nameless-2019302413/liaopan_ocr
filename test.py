import difflib
# # 对比
file = open(r".\picture\xiaowangzi.txt",
             'r')  # 打开文件
text = file.read()  # 读取文件内容

file_1 = open(r"result.txt",
             'r')  # 打开文件
text_1 = file.read()  # 读取文件内容

text1_lines = text.splitlines()
text2_lines = text_1.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)

print("\n".join(list(diff)))































































