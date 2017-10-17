#! /usr/bin/env python
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
reload(sys)
sys.setdefaultencoding('utf8')
#摘要  http://bosonnlp.com/analysis/summary?percentage=0.3
#0.3。 0.2 0.5
#词性情感  http://bosonnlp.com/analysis/sentiment?analysisType=news
#分类      http://bosonnlp.com/analysis/category
#实体识别   http://bosonnlp.com/analysis/ner?category=&sensitivity=5
#1-5
#依存文法语义树 http://bosonnlp.com/analysis/dependency_tree
#词性分析分词 http://bosonnlp.com/analysis/tag
#摘要？  http://bosonnlp.com/analysis/depend
#关键词   http://bosonnlp.com/analysis/key
#语义联想 http://bosonnlp.com/analysis/suggest

class nlpc():
    def __init__(self):
        self.idict={"init":{"url":"http://bosonnlp.com/demo?source=home-banner","tps":"cookie","tps1":""},
        "zydj":{'url':"http://bosonnlp.com/analysis/summary?percentage=0.1","tps":"摘要等级0.2 0.3。 0.5","tps1":""},
        "qg":{'url':"http://bosonnlp.com/analysis/sentiment?analysisType=news","tps":"语义情感  new 可选配置","tps1":"1"},
        "fl":{'url':"http://bosonnlp.com/analysis/category","tps":"分类 语义","tps1":""},
        "stsb":{'url':"http://bosonnlp.com/analysis/ner?category=&sensitivity=5","tps":"实体识别  关键实体识别识别等级1-5","tps1":"1"},
        "wf":{'url':"http://bosonnlp.com/analysis/dependency_tree","tps":"语义依据 文法 树","tps1":""},
        "fc":{'url':"http://bosonnlp.com/analysis/tag","tps":"词性分析,分词","tps1":""},
        "zy":{'url':"http://bosonnlp.com/analysis/depend","tps":"   摘要,分词权重","tps1":"1"},
        "gj":{'url':"http://bosonnlp.com/analysis/key","tps":"关键词","tps1":""},
        "lx":{'url':"http://bosonnlp.com/analysis/suggest","tps":"语义联想词","tps1":""}
        }
        self.url=""
        self.data = ""
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.seturlkey("init")
        self.request()

    def setdata(self,strx):
        rex = re.compile(r'^【.*?】|（.*?）$')
        self.data=re.sub(rex, "", strx)
        return self.data

    def seturlkey(self,keystr):
        self.url= self.idict[keystr]["url"]
        return self.url

    def request(self):
        # respdata = self.opener.open(self.url).read()
        if self.data:
            # self.data=self.dataformater(self.data)
            params={"data":self.data}
            params=urllib.urlencode(params)
            respdata=self.opener.open(self.url,params).read()
            # print "data: %s" %str(self.data)
        else:
            respdata=self.opener.open(self.url).read()
        return respdata

    def qgout(self,x):
        x = re.findall('[-+]?[0-9]*\.[0-9]*', x)
        o = float(x[0])
        # print o
        if 0.5 < float(o):
            t= "好 %s" % str(int(o * 10 - 5))
            # t="good"
        else:
            t="坏 %s" % str(int(10 - o * 10 - 5))
            # t="bad"
        return t

    def zyout(self,k):
        if not k: return
        # print k
        x = json.loads(k[1:k.rfind("]")])
        # print x
        sti=[]

        for si in x:
            st = ""
            for i in x[si]:
                st = st + "  " + str(i)
            print st
            sti.append(st)
        return sti

    def datatype(self,indexs):
        al = "体育 教育 财经 社会 娱乐 军事 国内 科技 互联网 房产 国际 女人 汽车 游戏"
        ar= al.split(" ")
        i=int(indexs[1])
        if i:return ar[i]
        return "err"
        # al=["体育" 教育 财经 社会 娱乐 军事 国内 科技 互联网 房产 国际 女人 汽车 游戏]
    def run(self,urlkey,data=""):
        if not data: return
        self.setdata(data)
        self.seturlkey(urlkey)
        x= self.request()
        # print x
        if "zydj" in urlkey:
            return str(x).replace("\n","")
        if "stsb" in urlkey:
            pass
            return x
        if "fl" in urlkey:
            return self.datatype(x)
        if "zy" in urlkey:
            return self.zyout(x)
        if "qg" in urlkey:
            return self.qgout(x)
        return x
    def start(self,data):
        # print type(data),data
        if type(data)==str:
            a = self.run("qg", data)
            # b = self.run("zydj", data)
            c = self.run("fl", data)
            # d=t.run("zy",data)
            # x=("分类:\n" + str(c) + "\n趋势:\n" + str(a) + "\n摘要:\n" + str(b) + "\n" )
            x=("分类:\n" + str(c) + "\n趋势:\n" + str(a)  )
            # i,createTime, id, country, asset, content
            return x
        if type(data)==list or type(data)==tuple:
            idata=data
            # idata[4]=data[4]
            idata[3] = self.run("qg", idata[5])
            # b = self.run("zydj", data)
            idata[4] = self.run("fl", idata[5])
            idata[5]=data[5]
            return idata

    def startArr(self,Arraydata):
        returndata=[]
        for data in Arraydata:
            returndata.append(self.start(data))
        return returndata



if __name__ == "__main__":
    print "start"
    t=nlpc()
    # # data="中金岭南(000060).10月12日晚发布业绩预告，预计前三季净利为8亿元-9亿元，同比增长388%-449%。报告期，公司严控生产经营成本，主产品铅锌金属市场价较去年同期上涨。"
    t.url="http://api.wallstreetcn.com/v2/livenews?limit=3&callback=jQuery213046828437503427267_"+ str(time.time())
    i=t.request()
    print i
    print time.time()

