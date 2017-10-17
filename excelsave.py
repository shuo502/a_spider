#! /usr/bin python
# -*- coding: UTF-8 –*-
import urllib
import urllib2
import cookielib
import json
import sys
import time
import xlwt
import re
import subprocess
import nlp
reload(sys)
sys.setdefaultencoding('utf8')


filename = "data.xls"
class excelsave():
    def __init__(self):
        self.count = 0
        self.reqindex = 0
        self.sheetindex = 1
        self.nextRow = 0
        self.filename = filename
        if self.filename[self.filename.rfind('.') + 1:] != 'xls' and self.filename[
                                                                     self.filename.rfind('.') + 1:] != 'xlsx':
            print 'Wrong format of filename, please select *.xls and *.xlsx to store result'
            return

        self.excel = xlwt.Workbook(encoding='utf-8')
        self.table = self.excel.add_sheet('wallstreet' + str(self.sheetindex), cell_overwrite_ok=True)

    def saveArr(self,dataArr):
        for data in dataArr:
            i,createTime,important,country,asset,content=data
            pass
            try:
                if self.nextRow >= 60000:
                    # reached the maximum of single sheet, create new sheet
                    self.sheetindex += 1
                    self.table = self.excel.add_sheet(str(important) + str(self.sheetindex), cell_overwrite_ok=True)
                    self.nextRow = 0

                self.table.write(self.nextRow, 0, i)
                self.table.write(self.nextRow, 1, createTime)
                self.table.write(self.nextRow, 2, important)
                self.table.write(self.nextRow, 3, country)
                self.table.write(self.nextRow, 4, asset)
                self.table.write(self.nextRow, 5, content)

                self.nextRow += 1
                self.count += 1
            except ValueError, e:
                print e.reason

    def save(self,data):
        for paresData in data:
            self.saveArr(paresData)
        self.excel.save(self.filename)