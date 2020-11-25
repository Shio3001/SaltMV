# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import main_user_CUI as main_user  # GUI処分 CUI中継操作

# set
from info_userCUI.Visualization import printlayer

from info_userCUI.EditPointFile import set_point  # CUI 操作に関するファイル GUI処分
from info_userCUI.EditPointFile import edit_point  # CUI 操作に関するファイル GUI処分 set_pointで設定したものを編集するやつ
from info_toset.PointFile import main_point  # 内部処理
# setend

# out

# outend

# 統括ファイル
from info_toset import info_toset_rally as set_rally  # 設定などを行う(内部)
from info_userCUI import info_userCUI_rally as userCUI_rally  # 設定などを行う(CUI)
from info_toout import info_toout_rally as out_rally  # 書き出す


import elements

# GUI処分ファイル・・・GUIにした時に削除するファイル
# CUI中継・・・CUIでの操作を担う部分
#
# 返却時には layer , 状態 でやりとりを行うようにする事
#
# 管理,設定(入力)と生成(出力)は完全分離しろ
#
# CHK_ ・・・保留
# EXC ・・・状態を表す


if __name__ == "__main__":
    print("コマンドライン からの入力を確認")

# 各種ファイルを設定 一度きりやしベタがき
set_rally_Center = set_rally.Center(main_point)  # 情報入力関連をまとめてやってくれる
userCUI_rally_Center = userCUI_rally.Center(set_point, edit_point, printlayer)  # CUI入力関連

out_rally_Center = out_rally.Center()  # 情報出力関連をまとめてやってくれる


class Center:
    def __init__(self):
        self.layer_group = []  # 一番重要だと思われ

        self.main_user_Center = main_user.Center()  # ユーザー操作を司る

    def Main(self):
        layer_group = self.main_user_Center.UserNextSelect(copy.deepcopy(self.layer_group), elements, userCUI_rally_Center)  # 次の選択を担うファイルへ送信


main_Center = Center()
main_Center.Main()

# まだ一回きりしか操作できないようになってる
# git確認4
