from PIL import Image
from ahk import AHK
import cv2
import numpy as np
from mss import mss
import ctypes
from ctypes.wintypes import HWND, DWORD, RECT
from time import sleep
import pyautogui

window_title = "NoxPlayer"
img_list_selectbox = ["img/selectbox_button.png"]

def GetTitle(window_title):
    ahk = AHK()
    wins = list(ahk.windows())
    titles = [win.title for win in wins]
    for t in titles:
        if window_title in t:
            print("found")
            return t
        
# ウィンドウの位置とサイズを取得
def GetWindowRectFromName(TargetWindowTitle):
    hwnd = ctypes.windll.user32.FindWindowW(None, TargetWindowTitle)
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd,ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom

# スクリーンショットを撮影する
def SCT(bbox):
    with mss() as sct:
        img = sct.grab(bbox)
    return img

# 画像を表示する
def img_show(window_name, img, position=(0, 0)):
    cv2.imshow(window_name, img)
    cv2.moveWindow(window_name, position[0], position[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 画像検知処理
# 閾値の設定
_THRESHOLD = 0.8
class TemplateMatching():
    def __init__(self, img, top_left):
        self.img2 = img.copy()
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.top_left = top_left
    def click_(self, w, h):
        click_location = [self.top_left[0]+self.loc[1][0]+w/2, self.top_left[1]+self.loc[0][0]+h/2]
        pyautogui.click(click_location)
    def close_button(self):
        template = cv2.imread('img/close_button.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        self.loc = np.where(res >= _THRESHOLD)
        if self.loc[0].size > 0:
            cv2.rectangle(self.img2, [self.loc[1][0], self.loc[0][0]], [self.loc[1][0] + w, self.loc[0][0] + h], (0,0,255), 2)
            self.click_(w, h)
        return self.img2
    def ok_button(self):
        template = cv2.imread('img/OK_button.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        self.loc = np.where(res >= _THRESHOLD)
        if self.loc[0].size > 0:
            cv2.rectangle(self.img2, [self.loc[1][0], self.loc[0][0]], [self.loc[1][0] + w, self.loc[0][0] + h], (0,0,255), 2)
            self.click_(w, h)
        return self.img2
    def selectbox_button(self):
        template = cv2.imread('img/selectbox_button.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        self.loc = np.where(res >= _THRESHOLD)
        if self.loc[0].size > 0:
            cv2.rectangle(self.img2, [self.loc[1][0], self.loc[0][0]], [self.loc[1][0] + w, self.loc[0][0] + h], (0,0,255), 2)
            self.click_(w, h)
        return self.img2
    def tap_screen(self):
        template = cv2.imread('img/tap_screen.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        self.loc = np.where(res >= _THRESHOLD)
        if self.loc[0].size > 0:
            cv2.rectangle(self.img2, [self.loc[1][0], self.loc[0][0]], [self.loc[1][0] + w, self.loc[0][0] + h], (0,0,255), 2)
            self.click_(w, h)
        return self.img2
    def retry_button(self):
        template = cv2.imread('img/retry_button.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        self.loc = np.where(res >= _THRESHOLD)
        if self.loc[0].size > 0:
            cv2.rectangle(self.img2, [self.loc[1][0], self.loc[0][0]], [self.loc[1][0] + w, self.loc[0][0] + h], (0,0,255), 2)
            self.click_(w, h)
        return self.img2

template_list = ["selectbox_button","ok_button", "tap_screen", "retry_button","close_button"]

# デスクトップキャプチャーを起動する
def main():
    TargetWindowTitle = GetTitle(window_title)
    if TargetWindowTitle is None:
        input("ウィンドウが見つかりませんでした。")
        exit()
    
    # ウィンドウの初期化
    cv2.namedWindow('Real-time Tsumu', cv2.WINDOW_NORMAL)
    i = 0
    while True:
        i += 1
        bbox = GetWindowRectFromName(TargetWindowTitle)
        img = SCT(bbox)   # スクショを撮る
        # face_rects, track_window = ColorDetection(img)
        # img2 = cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h), color=(0, 0, 255), thickness=5)
        # x, y, w, h = track_window
        img_np = np.array(img) # PIL型からOpenCV型に変換
        # img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        for te in template_list[0:4:1]:
            img_detect = getattr(TemplateMatching(img_np, [bbox[0], bbox[1]]), te)()
        if i == 5:
            img_detect = TemplateMatching(img_np, [bbox[0], bbox[1]]).close_button()
            i = 0
        #img_detect = TemplateMatching(img_np, [bbox[0], bbox[1]]).retry_button()
        # 画像を表示する
        cv2.imshow('Real-time Tsumu', img_detect)
        # window位置の変更
        cv2.moveWindow('Real-time Tsumu', bbox[2], bbox[1])
        # windouwサイズの変更
        cv2.resizeWindow('Real-time Tsumu', bbox[2]-bbox[0], bbox[3]-bbox[1])
        # escape sequence
        # ESC to escape
        k = cv2.waitKey(1) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            return
        # or topleft mouse to escape
        if AHK().mouse_position == (0, 0):
            cv2.destroyAllWindows()
            return
        # 任意の待機時間を設ける
        # sleep(0.1)
        """except:
            continue"""

if __name__ == "__main__":
    main()