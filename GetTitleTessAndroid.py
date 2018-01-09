# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索


from PIL import Image
import os
import pytesseract
import webbrowser
import subprocess
import numpy as np


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')
    # 删除原有截图
    os.system("adb shell rm /sdcard/screenshot.png")

# 不成功待测试
def pull_screenshot2():
    process = subprocess.Popen('adb shell screencap -p ', shell=True, stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read()
    #binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
    #img = np.array(binary_screenshot)
    print(binary_screenshot)
    f = open('screenshot.png', 'wb')
    f.write(binary_screenshot)
    f.close()

# 截图已存在则删除，增加容错
if os.path.isfile('screenshot.png'):
    try:
        os.remove('screenshot.png')
    except Exception:
        pass

pull_screenshot()
img = Image.open("./screenshot.png")

# 切割题目位置，左上角坐标和右下角坐标
question = img.crop((50, 350, 1000, 560)) # 坚果 pro1
choices = img.crop((75, 535, 990, 1150))

#region = img.crop((75, 315, 1167, 789)) # iPhone 7P

# tesseract 路径
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
# 语言包目录
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

# lang 指定中文简体
text = pytesseract.image_to_string(question, lang='chi_sim', config=tessdata_dir_config)
text = text.replace("\n", "")[2:]

#text2 = pytesseract.image_to_string(choices, lang='chi_sim', config=tessdata_dir_config)
#text2 = text2.replace("\n", "")

print(text)
#print(text2)
webbrowser.open('https://baidu.com/s?wd='+text)

image = Image.open("./screenshot.png")
question,choices = ocr_img(image)

print("识别结果:")
print(question)
print(choices)
