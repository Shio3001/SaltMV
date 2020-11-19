# coding:utf-8
import sys
import numpy
import os


class EditDataElement_Operation:
    def __init__(self, SetImport_Main, SetImport_Size, SetImport_Color, SetImport_Cal):
        self.Import_Main = SetImport_Main
        self.Import_Size = SetImport_Size
        self.Import_Color = SetImport_Color
        self.Import_Cal = SetImport_Cal

        print(self.Import_Main, self.Import_Size, self.Import_Color, self.Import_Cal)


class EditDataElement_Information:
    def __init__(self, SetaddfntSize, SetNewTextString, SetRGBdata):
        self.addfntSize = SetaddfntSize
        self.NewTextString = SetNewTextString
        self.RGBdata = SetRGBdata
