import ctypes
import tkinter as tk

import cv2

# ----------------------------------------------------------------------
# 	構造体などの定義
# ----------------------------------------------------------------------
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0

# StretchBlt() Modes
BLACKONWHITE = 1
WHITEONBLACK = 2
COLORONCOLOR = 3
HALFTONE = 4


class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.wintypes.LONG),
        ('top', ctypes.wintypes.LONG),
        ('right', ctypes.wintypes.LONG),
        ('bottom', ctypes.wintypes.LONG)
    ]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', ctypes.wintypes.DWORD),
        ('biWidth', ctypes.wintypes.LONG),
        ('biHeight', ctypes.wintypes.LONG),
        ('biPlanes', ctypes.wintypes.WORD),
        ('biBitCount', ctypes.wintypes.WORD),
        ('biCompression', ctypes.wintypes.DWORD),
        ('biSizeImage', ctypes.wintypes.DWORD),
        ('biXPelsPerMeter', ctypes.wintypes.LONG),
        ('biYPelsPerMeter', ctypes.wintypes.LONG),
        ('biClrUsed', ctypes.wintypes.DWORD),
        ('biClrImportant', ctypes.wintypes.DWORD)
    ]


class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ('rgbBlue', ctypes.wintypes.BYTE),
        ('rgbGreen', ctypes.wintypes.BYTE),
        ('rgbRed', ctypes.wintypes.BYTE),
        ('rgbReserved', ctypes.wintypes.BYTE)
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', RGBQUAD * 256)
    ]
