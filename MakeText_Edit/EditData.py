# coding:utf-8
import sys
import numpy
import os


class EditDataElement:
    def __init__(self):
        self.addfntSize = []
        self.NewTextString = ""
        self.RGBdata = []

        self.Import_Main = None
        self.Import_Cal = None
        self.Import_Size = None
        self.Import_Color = None

    def SetElement_Text(self, SetaddfntSize, SetNewTextString, SetRGBdata):
        self.addfntSize = SetaddfntSize
        self.NewTextString = SetNewTextString
        self.RGBdata = SetRGBdata

    def SetImport_Text(self, SetImport_Main, SetImport_Size, SetImport_Color, SetImport_Cal):
        self.Import_Main = SetImport_Main
        self.Import_Size = SetImport_Size
        self.Import_Color = SetImport_Color
        self.Import_Cal = SetImport_Cal
