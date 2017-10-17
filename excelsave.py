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

    def saveData(self, results):
        if results is None:
            return

        # write data to excel
        for data in results:

            createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data['createdAt'])))
            important = data['importance']
            content = data['contentHtml']
            country = ''
            asset = ''
            cataset = data['categorySet']
            if cataset is not None:
                catagory = cataset.split(',')
                if catagory is not None:
                    if '9' in catagory:
                        country = '中国'
                    elif '10' in catagory:
                        country = '美国'
                    elif '11' in catagory:
                        country = '欧元区'
                    elif '12' in catagory:
                        country = '日本'
                    elif '13' in catagory:
                        country = '英国'
                    elif '14' in catagory:
                        country = '澳洲'
                    elif '15' in catagory:
                        country = '加拿大'
                    elif '16' in catagory:
                        country = '瑞士'
                    else:
                        country = "其它"

                if catagory is not None:
                    if '1' in catagory:
                        asset = '外汇'
                    elif '2' in catagory:
                        asset = '股市'
                    elif '3' in catagory:
                        asset = '商品'
                    elif '4' in catagory:
                        asset = '债市'
                    else:
                        asset = '其它'

            # cut out <p> and </p>
            content = re.compile(r'\<\/?p\>').sub('', content)

            try:
                if self.nextRow >= 60000:
                    # reached the maximum of single sheet, create new sheet
                    self.sheetindex += 1
                    self.table = self.excel.add_sheet('wallstreet' + str(self.sheetindex), cell_overwrite_ok=True)
                    self.nextRow = 0

                self.table.write(self.nextRow, 0, "wallstreet")
                self.table.write(self.nextRow, 1, createTime)
                self.table.write(self.nextRow, 2, int(important))
                self.table.write(self.nextRow, 3, country)
                self.table.write(self.nextRow, 4, asset)
                self.table.write(self.nextRow, 5, content)

                self.nextRow += 1
                self.count += 1
            except ValueError, e:
                print e.reason

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