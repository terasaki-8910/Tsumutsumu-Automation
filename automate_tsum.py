import os
import cv2
import numpy as np
from subprocess import run,PIPE
import pyautogui

# グローバル変数の宣言
_DIR_NOX = r"C:\Program Files (x86)\Nox\bin"
_DIR_ANDROID_CAPTURE = r"\sdcard\_capture.png"
_NAME_INTERNAL_CAPTURE_FOLDER = "pics"
_DIR_INTERNAL_CAPTURE = r"C:\Program Files (x86)\Nox\bin\pics\_capture.png"
_THRESHOLD = 0.9 #類似度

def doscmd(directory, command):
    completed_process = run(command, stdout=PIPE, shell=True, cwd=directory, universal_newlines=True, timeout=10)
    return completed_process.stdout

def send_cmd_to_adb(cmd):
    return doscmd(_DIR_NOX, cmd)

def tap(x, y):
    _cmd = "nox_adb shell input touchscreen tap " + str(x) + " " + str(y)
    send_cmd_to_adb(_cmd)

def show_log():
    _cmd = "nox_adb logcat -d"
    _pipe = send_cmd_to_adb(_cmd)
    return _pipe

# 画像所の指定した画像をタップさせる
# 手順1 スクリーンショットを取る
def capture_screen(dir_android, folder_name):
    _cmd = "nox_adb shell screencap -p " + dir_android
    _pipe = send_cmd_to_adb(_cmd)

    _cmd = "nox_adb pull " + dir_android+ " " + folder_name
    send_cmd_to_adb(_cmd)

# 手順2 テンプレートに一致する部分の中心座標を取得する
# _DIR_INTERNAL_CAPTURE = "D:/Program Files/Nox/bin/pics/_capture.png"
# _DIR_TEMP = "img/temp.png"
# _THRESHOLD = 0.9 #類似度
def get_center_position_from_tmp(dir_input, dir_tmp):
    _input = cv2.imread(dir_input)
    _temp = cv2.imread(dir_tmp)

    gray = cv2.cvtColor(_input, cv2.COLOR_RGB2GRAY)
    temp = cv2.cvtColor(_temp, cv2.COLOR_RGB2GRAY)

    _h, _w = _temp.shape

    _match = cv2.matchTemplate(_input, _temp, cv2.TM_CCOEFF_NORMED)
    _loc = np.where(_match >= _THRESHOLD)
    try:
        _x = _loc[1][0]
        _y = _loc[0][0]
        return _x + _w / 2, _y + _h / 2
    except IndexError as e:
        return -1, -1

# 手順3 取得した座標をタップする
def tap_position(x, y):
    tap(x, y)
    
if __name__ == "__main__":
    _DIR_TEMP = r"\img\start.png"
    capture_screen(_DIR_ANDROID_CAPTURE, _NAME_INTERNAL_CAPTURE_FOLDER)
    x, y = get_center_position_from_tmp(_DIR_INTERNAL_CAPTURE, _DIR_TEMP)