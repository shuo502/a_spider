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
        # for si in x:
        #     ss="".join(x[si])
        #     print ss
        #     sti.append(ss)
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
    def start(self,data=""):
        a = self.run("qg", data)
        # b = self.run("zydj", data)
        c = self.run("fl", data)
        # d=t.run("zy",data)
        # x=("分类:\n" + str(c) + "\n趋势:\n" + str(a) + "\n摘要:\n" + str(b) + "\n" )
        x=("分类:\n" + str(c) + "\n趋势:\n" + str(a)  )
        return x

if __name__ == "__main__":
    print "start"
    t=nlpc()
    # # data="中金岭南(000060).10月12日晚发布业绩预告，预计前三季净利为8亿元-9亿元，同比增长388%-449%。报告期，公司严控生产经营成本，主产品铅锌金属市场价较去年同期上涨。"
    # # # t.start(data)
    t.url="http://api.wallstreetcn.com/v2/livenews?limit=3&callback=jQuery213046828437503427267_"+ str(time.time())
    # t.url="http://api.wallstreetcn.com/v2/livenews?limit=3&callback=jQuery213046828437503427267_1433944460455"+

    i=t.request()
    # # i="a(ssdfsdfd)a"

    # print type(k),k
    # detailPost
    print i

            # id=""
            # newid=""
            # if wid>wnewid:
            #     pass
            # for i in range(id,newid):
            #     print i


    print time.time()

            # x={u'paginator': {u'last': u'https://api.wallstreetcn.com/v2/livenews?status=published&cid%5B0%5D=9&importance=3&order=-created_at&page=2068&channelId=1&extractImg=0&extractText=0', u'next': u'https://api.wallstreetcn.com/v2/livenews?status=published&cid%5B0%5D=9&importance=3&order=-created_at&page=2&channelId=1&extractImg=0&extractText=0', u'limit': 2, u'total': 4136, u'page': 1, u'previous': u'https://api.wallstreetcn.com/v2/livenews?status=published&cid%5B0%5D=9&importance=3&order=-created_at&page=1&channelId=1&extractImg=0&extractText=0'}, u'results': [{u'commentStatus': u'open', u'text': {u'contentFollowup': u'', u'contentAnalysis': u'', u'contentExtra': u'<img src="https://wpimg.wallstcn.com/c7b45424-c9a6-44df-aebd-642bf2c34dfe.png"/>'}, u'image': u'https://wpimg.wallstcn.com/c7b45424-c9a6-44df-aebd-642bf2c34dfe.png', u'userId': u'2815', u'moreText': None, u'commentCount': u'0', u'categorySet': u'9,2', u'video': None, u'updatedAt': u'1503279525', u'node_format': u'\u52a0\u7c97', u'id': u'507816', u'imageCount': u'0', u'imageUrls': [u'https://wpimg.wallstcn.com/c7b45424-c9a6-44df-aebd-642bf2c34dfe.png'], u'title': u'\u8bc1\u76d1\u4f1a\u79f0\uff0c\u5bf9\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u6d89\u53ca\u7684\u975e\u516c\u5f00\u53d1\u884c\u80a1\u7968\u4e8b\u9879\u4f5c\u4e3a\u4e2a\u6848\u5904\u7406\uff0c\u9002\u75282\u670817\u65e5\u8bc1\u76d1\u4f1a\u518d\u878d\u8d44\u5236\u5ea6\u4fee\u8ba2\u524d\u7684\u89c4\u5219\u3002\u8bc1\u76d1\u4f1a\u6df1\u523b\u8ba4\u8bc6\u548c\u7406\u89e3\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u5bf9\u4e8e\u6df1\u5316\u56fd\u4f01\u6539\u9769\u5177\u6709\u5148\u884c\u5148\u8bd5\u7684\u91cd\u5927\u610f\u4e49\u3002', u'data': None, u'moreImgs': [u'https://wpimg.wallstcn.com/c7b45424-c9a6-44df-aebd-642bf2c34dfe.png'], u'sourceName': None, u'hasMore': u'1', u'createdAt': u'1503243333', u'type': u'news', u'node_color': u'\u7ea2\u8272', u'status': u'published', u'sourceUrl': None, u'star': False, u'importance': u'3', u'detailPost': None, u'channelSet': u'2,1', u'videoCount': u'0', u'viewCount': u'0', u'contentText': u'\u8bc1\u76d1\u4f1a\u79f0\uff0c\u5bf9\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u6d89\u53ca\u7684\u975e\u516c\u5f00\u53d1\u884c\u80a1\u7968\u4e8b\u9879\u4f5c\u4e3a\u4e2a\u6848\u5904\u7406\uff0c\u9002\u75282\u670817\u65e5\u8bc1\u76d1\u4f1a\u518d\u878d\u8d44\u5236\u5ea6\u4fee\u8ba2\u524d\u7684\u89c4\u5219\u3002\u8bc1\u76d1\u4f1a\u6df1\u523b\u8ba4\u8bc6\u548c\u7406\u89e3\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u5bf9\u4e8e\u6df1\u5316\u56fd\u4f01\u6539\u9769\u5177\u6709\u5148\u884c\u5148\u8bd5\u7684\u91cd\u5927\u610f\u4e49\u3002', u'shareCount': u'0', u'codeType': u'markdown', u'contentHtml': u'<p>\u8bc1\u76d1\u4f1a\u79f0\uff0c\u5bf9\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u6d89\u53ca\u7684\u975e\u516c\u5f00\u53d1\u884c\u80a1\u7968\u4e8b\u9879\u4f5c\u4e3a\u4e2a\u6848\u5904\u7406\uff0c\u9002\u75282\u670817\u65e5\u8bc1\u76d1\u4f1a\u518d\u878d\u8d44\u5236\u5ea6\u4fee\u8ba2\u524d\u7684\u89c4\u5219\u3002\u8bc1\u76d1\u4f1a\u6df1\u523b\u8ba4\u8bc6\u548c\u7406\u89e3\u4e2d\u56fd\u8054\u901a\u6df7\u6539\u5bf9\u4e8e\u6df1\u5316\u56fd\u4f01\u6539\u9769\u5177\u6709\u5148\u884c\u5148\u8bd5\u7684\u91cd\u5927\u610f\u4e49\u3002</p>'}, {u'commentStatus': u'open', u'text': {u'contentFollowup': u'', u'contentAnalysis': u'', u'contentExtra': u'<p>\u636e\u8bc1\u76d1\u4f1a\u8054\u5408\u516c\u5b89\u90e8\u4e13\u9898\u8282\u76ee\u300a\u5927\u6570\u636e\u6355\u201c\u9f20\u201d\u8bb0\u300b\uff0c\u8bc1\u76d1\u4f1a\u7a3d\u67e5\u5c40\u4eba\u5458\u8868\u793a\uff0c\u8d44\u4ea7\u7ba1\u7406\u4eba\u5458\u505a\u8001\u9f20\u4ed3\uff0c\u662f\u4e00\u79cd\u80cc\u4fe1\u884c\u4e3a\uff0c\u8bc1\u76d1\u4f1a\u5bf9\u8001\u9f20\u4ed3\u96f6\u5bb9\u5fcd\u3001\u5168\u8986\u76d6\u3001\u51fa\u91cd\u62f3\u3002</p><p>\u53e6\u636e\u8bc1\u76d1\u4f1a\u5468\u4e94\u6d88\u606f\uff0c\u4e0b\u4e00\u6b65\uff0c\u8bc1\u76d1\u4f1a\u4e00\u65b9\u9762\u5c06\u79ef\u6781\u63a2\u7d22\u8de8\u90e8\u95e8\u4fe1\u606f\u5171\u4eab\u3001\u8054\u5408\u68c0\u67e5\uff0c\u5065\u5168\u7efc\u5408\u9632\u63a7\u957f\u6548\u673a\u5236\uff1b\u63a8\u52a8\u51fa\u53f0\u201c\u8001\u9f20\u4ed3\u201d\u53f8\u6cd5\u89e3\u91ca\uff0c\u660e\u786e\u6267\u6cd5\u6807\u51c6\u3002</p>'}, u'image': u'', u'userId': u'2815', u'moreText': u'<p>\u636e\u8bc1\u76d1\u4f1a\u8054\u5408\u516c\u5b89\u90e8\u4e13\u9898\u8282\u76ee\u300a\u5927\u6570\u636e\u6355\u201c\u9f20\u201d\u8bb0\u300b\uff0c\u8bc1\u76d1\u4f1a\u7a3d\u67e5\u5c40\u4eba\u5458\u8868\u793a\uff0c\u8d44\u4ea7\u7ba1\u7406\u4eba\u5458\u505a\u8001\u9f20\u4ed3\uff0c\u662f\u4e00\u79cd\u80cc\u4fe1\u884c\u4e3a\uff0c\u8bc1\u76d1\u4f1a\u5bf9\u8001\u9f20\u4ed3\u96f6\u5bb9\u5fcd\u3001\u5168\u8986\u76d6\u3001\u51fa\u91cd\u62f3\u3002</p><p>\u53e6\u636e\u8bc1\u76d1\u4f1a\u5468\u4e94\u6d88\u606f\uff0c\u4e0b\u4e00\u6b65\uff0c\u8bc1\u76d1\u4f1a\u4e00\u65b9\u9762\u5c06\u79ef\u6781\u63a2\u7d22\u8de8\u90e8\u95e8\u4fe1\u606f\u5171\u4eab\u3001\u8054\u5408\u68c0\u67e5\uff0c\u5065\u5168\u7efc\u5408\u9632\u63a7\u957f\u6548\u673a\u5236\uff1b\u63a8\u52a8\u51fa\u53f0\u201c\u8001\u9f20\u4ed3\u201d\u53f8\u6cd5\u89e3\u91ca\uff0c\u660e\u786e\u6267\u6cd5\u6807\u51c6\u3002</p>', u'commentCount': u'0', u'categorySet': u'2,9', u'video': None, u'updatedAt': u'1499522698', u'node_format': u'\u52a0\u7c97', u'id': u'484760', u'imageCount': u'0', u'imageUrls': [], u'title': u'\u3010\u7126\u70b9\u8bbf\u8c08\u64ad\u51fa\u8bc1\u76d1\u4f1a\u516c\u5b89\u90e8\u4e13\u9898\u8282\u76ee\uff1a\u5927\u6570\u636e\u6355\u201c\u9f20\u201d\u8bb0\u3011\u8282\u76ee\u6307\u51fa\uff0c\u4e00\u4e9b\u8fc7\u53bb\u5f88\u5c11\u8fdb\u5165\u6267\u6cd5\u89c6\u91ce\u7684\u5c97\u4f4d\uff0c\u6bd4\u5982\u57fa\u91d1\u4ea4\u6613\u5458\u3001\u4fdd\u9669\u8d44\u7ba1\u4ece\u4e1a\u4eba\u5458\uff0c\u751a\u81f3\u662f\u603b\u76d1\u7ea7\u3001\u9ad8\u7ba1\u7ea7\u7684\u4eba\u5458\uff0c\u4e5f\u73a9\u8d77\u4e86\u201c\u8001\u9f20\u4ed3\u201d\uff0c\u800c\u4e14\u624b\u6cd5\u4e5f\u6709\u65b0\u53d8\u5316\uff0c\u8d5a...', u'data': None, u'moreImgs': [], u'sourceName': None, u'hasMore': u'1', u'createdAt': u'1499517126', u'type': u'news', u'node_color': u'\u7ea2\u8272', u'status': u'published', u'sourceUrl': None, u'star': False, u'importance': u'3', u'detailPost': {u'count': u'3769', u'imageUrl': u'https://wpimg.wallstcn.com/3e51993b-1b1f-4f97-86ad-0fd5aeb2ec07.jpg', u'sourceUrl': u'', u'summaryHtml': u'\u8bc1\u76d1\u4f1a\u5468\u4e94\u6307\u51fa\uff0c2014\u5e74\u4ee5\u6765\uff0c\u8bc1\u76d1\u4f1a\u542f\u52a899\u8d77\u8001\u9f20\u4ed3\u6848\u4ef6\u8c03\u67e5\uff0c\u79fb\u4ea4\u53f8\u6cd5\u673a\u5173\u5904\u7406\u6848\u4ef683\u8d77\uff0c\u6d89\u6848\u91d1\u989d\u8fbe800\u4ebf\u5143\u3002\u8001\u9f20\u4ed3\u6210\u4e3a\u7ee7\u5185\u5e55\u4ea4\u6613\u540e\uff0c\u8bc1\u76d1\u4f1a\u79fb\u9001\u516c\u5b89\u673a\u5173\u8ffd\u7a76\u5211\u4e8b\u8d23\u4efb\u6bd4\u4f8b\u6700\u9ad8\u7684\u4e00\u7c7b\u6848\u4ef6\u3002', u'title': u'\u516c\u5b89\u90e8\u4e25\u6253\u201c\u8001\u9f20\u4ed3\u201d\u72af\u7f6a \u8bc1\u76d1\u4f1a\u79f0\u6d89\u6848\u91d1\u989d\u9ad8\u8fbe800\u4ebf\u5143', u'commentStatus': u'open', u'image': u'https://wpimg.wallstcn.com/3e51993b-1b1f-4f97-86ad-0fd5aeb2ec07.jpg', u'tags': [], u'categories': [{u'id': u'17', u'categoryName': u'\u4e2d\u56fd'}, {u'id': u'19', u'categoryName': u'\u7ecf\u6d4e'}], u'id': u'313956', u'commentCount': u'0', u'sourceName': u'', u'url': u'http://wallstreetcn.com/node/313956', u'codeType': u'html', u'assetTags': [], u'summary': u'\u8bc1\u76d1\u4f1a\u5468\u4e94\u6307\u51fa\uff0c2014\u5e74\u4ee5\u6765\uff0c\u8bc1\u76d1\u4f1a\u542f\u52a899\u8d77\u8001\u9f20\u4ed3\u6848\u4ef6\u8c03\u67e5\uff0c\u79fb\u4ea4\u53f8\u6cd5\u673a\u5173\u5904\u7406\u6848\u4ef683\u8d77\uff0c\u6d89\u6848\u91d1\u989d\u8fbe800\u4ebf\u5143\u3002\u8001\u9f20\u4ed3\u6210\u4e3a\u7ee7\u5185\u5e55\u4ea4\u6613\u540e\uff0c\u8bc1\u76d1\u4f1a\u79fb\u9001\u516c\u5b89\u673a\u5173\u8ffd\u7a76\u5211\u4e8b\u8d23\u4efb\u6bd4\u4f8b\u6700\u9ad8\u7684\u4e00\u7c7b\u6848\u4ef6\u3002', u'type': u'news', u'slug': u'otl1b3P1', u'createdAt': u'1499431299', u'user': {u'username': u'rslyx0704', u'url': u'http://s.wallstreetcn.com/users/100001393675', u'id': u'100001393675', u'avatar': u'https://dn-wscn-avatar.qbox.me/06/28/c3/photo.png', u'screenName': u'\u5218\u6021\u5fc3'}}, u'channelSet': u'2,1', u'videoCount': u'0', u'viewCount': u'0', u'contentText': u'\u3010\u7126\u70b9\u8bbf\u8c08\u64ad\u51fa\u8bc1\u76d1\u4f1a\u516c\u5b89\u90e8\u4e13\u9898\u8282\u76ee\uff1a\u5927\u6570\u636e\u6355\u201c\u9f20\u201d\u8bb0\u3011\u8282\u76ee\u6307\u51fa\uff0c\u4e00\u4e9b\u8fc7\u53bb\u5f88\u5c11\u8fdb\u5165\u6267\u6cd5\u89c6\u91ce\u7684\u5c97\u4f4d\uff0c\u6bd4\u5982\u57fa\u91d1\u4ea4\u6613\u5458\u3001\u4fdd\u9669\u8d44\u7ba1\u4ece\u4e1a\u4eba\u5458\uff0c\u751a\u81f3\u662f\u603b\u76d1\u7ea7\u3001\u9ad8\u7ba1\u7ea7\u7684\u4eba\u5458\uff0c\u4e5f\u73a9\u8d77\u4e86\u201c\u8001\u9f20\u4ed3\u201d\uff0c\u800c\u4e14\u624b\u6cd5\u4e5f\u6709\u65b0\u53d8\u5316\uff0c\u8d5a\u5f97\u662f\u76c6\u6ee1\u94b5\u6ee1\u3002', u'shareCount': u'0', u'codeType': u'markdown', u'contentHtml': u'<p>\u3010\u7126\u70b9\u8bbf\u8c08\u64ad\u51fa\u8bc1\u76d1\u4f1a\u516c\u5b89\u90e8\u4e13\u9898\u8282\u76ee\uff1a\u5927\u6570\u636e\u6355\u201c\u9f20\u201d\u8bb0\u3011\u8282\u76ee\u6307\u51fa\uff0c\u4e00\u4e9b\u8fc7\u53bb\u5f88\u5c11\u8fdb\u5165\u6267\u6cd5\u89c6\u91ce\u7684\u5c97\u4f4d\uff0c\u6bd4\u5982\u57fa\u91d1\u4ea4\u6613\u5458\u3001\u4fdd\u9669\u8d44\u7ba1\u4ece\u4e1a\u4eba\u5458\uff0c\u751a\u81f3\u662f\u603b\u76d1\u7ea7\u3001\u9ad8\u7ba1\u7ea7\u7684\u4eba\u5458\uff0c\u4e5f\u73a9\u8d77\u4e86\u201c\u8001\u9f20\u4ed3\u201d\uff0c\u800c\u4e14\u624b\u6cd5\u4e5f\u6709\u65b0\u53d8\u5316\uff0c\u8d5a\u5f97\u662f\u76c6\u6ee1\u94b5\u6ee1\u3002</p>'}]}
    # y= x['results'][1]["detailPost"]
    # y1= x['results'][1]["contentText"]
    # y2= x['results'][1]["moreText"]
    # y2= x['results'][1]["id"]
    # print y
    # print y1
    # print y2
    # # for i in x['results']:
    # #     data=i['updatedAt']
    # #     datb=i["contentText"]
    # #     # datc=i['contentHtml']
    # #     datd=i['moreText']
    # #     for j in i['text']:
    # #         print j, i['text'][j]
    # #
    # #     for n in i:
    # #         print n,i[n]
    # #     print data,"\n2",datb,"\n4",datd,"\n"
    # # j={u'count': u'3769', u'slug': u'otl1b3P1', u'sourceUrl': u'', u'summaryHtml': u'\u8bc1\u76d1\u4f1a\u5468\u4e94\u6307\u51fa\uff0c2014\u5e74\u4ee5\u6765\uff0c\u8bc1\u76d1\u4f1a\u542f\u52a899\u8d77\u8001\u9f20\u4ed3\u6848\u4ef6\u8c03\u67e5\uff0c\u79fb\u4ea4\u53f8\u6cd5\u673a\u5173\u5904\u7406\u6848\u4ef683\u8d77\uff0c\u6d89\u6848\u91d1\u989d\u8fbe800\u4ebf\u5143\u3002\u8001\u9f20\u4ed3\u6210\u4e3a\u7ee7\u5185\u5e55\u4ea4\u6613\u540e\uff0c\u8bc1\u76d1\u4f1a\u79fb\u9001\u516c\u5b89\u673a\u5173\u8ffd\u7a76\u5211\u4e8b\u8d23\u4efb\u6bd4\u4f8b\u6700\u9ad8\u7684\u4e00\u7c7b\u6848\u4ef6\u3002', u'title': u'\u516c\u5b89\u90e8\u4e25\u6253\u201c\u8001\u9f20\u4ed3\u201d\u72af\u7f6a \u8bc1\u76d1\u4f1a\u79f0\u6d89\u6848\u91d1\u989d\u9ad8\u8fbe800\u4ebf\u5143', u'commentStatus': u'open', u'imageUrl': u'https://wpimg.wallstcn.com/3e51993b-1b1f-4f97-86ad-0fd5aeb2ec07.jpg', u'tags': [], u'createdAt': u'1499431299', u'id': u'313956', u'commentCount': u'0', u'sourceName': u'', u'url': u'http://wallstreetcn.com/node/313956', u'codeType': u'html', u'assetTags': [], u'summary': u'\u8bc1\u76d1\u4f1a\u5468\u4e94\u6307\u51fa\uff0c2014\u5e74\u4ee5\u6765\uff0c\u8bc1\u76d1\u4f1a\u542f\u52a899\u8d77\u8001\u9f20\u4ed3\u6848\u4ef6\u8c03\u67e5\uff0c\u79fb\u4ea4\u53f8\u6cd5\u673a\u5173\u5904\u7406\u6848\u4ef683\u8d77\uff0c\u6d89\u6848\u91d1\u989d\u8fbe800\u4ebf\u5143\u3002\u8001\u9f20\u4ed3\u6210\u4e3a\u7ee7\u5185\u5e55\u4ea4\u6613\u540e\uff0c\u8bc1\u76d1\u4f1a\u79fb\u9001\u516c\u5b89\u673a\u5173\u8ffd\u7a76\u5211\u4e8b\u8d23\u4efb\u6bd4\u4f8b\u6700\u9ad8\u7684\u4e00\u7c7b\u6848\u4ef6\u3002', u'type': u'news', u'image': u'https://wpimg.wallstcn.com/3e51993b-1b1f-4f97-86ad-0fd5aeb2ec07.jpg', u'categories': [{u'id': u'17', u'categoryName': u'\u4e2d\u56fd'}, {u'id': u'19', u'categoryName': u'\u7ecf\u6d4e'}], u'user': {u'username': u'rslyx0704', u'url': u'http://s.wallstreetcn.com/users/100001393675', u'screenName': u'\u5218\u6021\u5fc3', u'id': u'100001393675', u'avatar': u'https://dn-wscn-avatar.qbox.me/06/28/c3/photo.png'}}
    # # for i in j:
    # #     print i,j[i]
    # nn={u'commentStatus': u'open', u'text': {u'contentFollowup': u'', u'contentAnalysis': u'', u'contentExtra': u''}, u'image': u'', u'userId': u'694840', u'moreText': None, u'commentCount': u'0', u'categorySet': None, u'video': None, u'updatedAt': u'1507830851', u'node_format': u'', u'id': u'532745', u'imageCount': u'0', u'imageUrls': [], u'title': u'\u7f8e\u56fd\u767d\u5bab\u5e55\u50da\u957fKelly\uff1a\u6211\u6ca1\u6709\u8f9e\u804c\uff0c\u4e5f\u4e0d\u4f1a\u88ab\u7279\u6717\u666e\u89e3\u96c7\uff0c\u6ca1\u89c9\u5f97\u6cae\u4e27\u3002\uff08\u7f8e\u5143\u6307\u6570\u6da80.03%\uff0c\u6682\u62a593.00\u3002\uff09', u'data': None, u'moreImgs': [], u'sourceName': None, u'hasMore': u'0', u'createdAt': u'1507830813', u'type': u'news', u'node_color': u'', u'status': u'published', u'sourceUrl': None, u'star': False, u'importance': u'1', u'detailPost': None, u'channelSet': u'1,0,0,4', u'videoCount': u'0', u'viewCount': u'0', u'contentText': u'\u7f8e\u56fd\u767d\u5bab\u5e55\u50da\u957fKelly\uff1a\u6211\u6ca1\u6709\u8f9e\u804c\uff0c\u4e5f\u4e0d\u4f1a\u88ab\u7279\u6717\u666e\u89e3\u96c7\uff0c\u6ca1\u89c9\u5f97\u6cae\u4e27\u3002\uff08\u7f8e\u5143\u6307\u6570\u6da80.03%\uff0c\u6682\u62a593.00\u3002\uff09', u'shareCount': u'0', u'codeType': u'markdown', u'contentHtml': u'<p>\u7f8e\u56fd\u767d\u5bab\u5e55\u50da\u957fKelly\uff1a\u6211\u6ca1\u6709\u8f9e\u804c\uff0c\u4e5f\u4e0d\u4f1a\u88ab\u7279\u6717\u666e\u89e3\u96c7\uff0c\u6ca1\u89c9\u5f97\u6cae\u4e27\u3002</p><p>\uff08\u7f8e\u5143\u6307\u6570\u6da80.03%\uff0c\u6682\u62a593.00\u3002\uff09</p>'}
    # for i in nn:
    #     print i,":",nn[i]