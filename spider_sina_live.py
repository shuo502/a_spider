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
import excelsave
reload(sys)
sys.setdefaultencoding('utf8')
#id=599648   news title id
#callback=t15077017   unix time


class sina():

    def __init__(self):
        self.spd=6
        # id=599648
        self.restr = []
        self.callback="t"+str(int(str(time.time())[0:8])-1)#time fen
        self.id=599927
        self.newid = 0
        self.url = ""
        self.wnewid=0
        self.wid=0
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def setspd(self,spd):
        self.spd=spd
        return self.spd
    def sinaurl(self):
        self.callback = "t" + str(int(str(time.time())[0:8]) - 1)  # time fen
        self.initsinaurl = 'http://live.sina.com.cn/zt/api/f/get/finance/globalnews1/index.htm?format=json&callback=' + str(self.callback) + '&id=' + str(self.id) + '&tag=0&pagesize=15&dire=f&dp'
        self.url=self.initsinaurl
        return self.initsinaurl

    def wallstreetcnurl(self):
        self.initwallstreetcnurl = "http://api.wallstreetcn.com/v2/livenews?limit=3&callback=jQuery213046828437503427267_" + str(time.time())
        self.url=self.initwallstreetcnurl
        return self.initwallstreetcnurl


    def setid(self,id):
        self.id=id
        return self.id

    def request(self):
        respdata = self.opener.open(self.url).read()
        return respdata

    def jsondata(self,results):
        if results is None:
            return
        self.restr=[]
        j=results
        r = j[j.find('(') + 1:j.rfind(');}')].decode('unicode_escape')

        p=re.compile(r"<(.*?)\\/a>")
        j=re.sub(p,"",r)#清除部分内容
        j = re.compile(r'\<\/?p\>').sub('', j)
        n=json.loads(j,strict=False)
        l=n["result"]["data"]
        l=sorted(l, key=lambda e: e.__getitem__('id'))
        if l:self.id=l[-1]["id"]
        self.newid=self.id
        print "新news id：%s" % str(self.newid)
        self.restr = []
        for data in l:
            iam,createTime, id, country, asset, icontent=["sina","","","","",""]
            createTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data['created_at'])))
            icontent=data["content"]
            # x = time.localtime(int(i["created_at"]))
            # sd = time.localtime(int(i["created_at"]))
            # print(time.strftime('%Y-%m-%d %H:%M:%S', x),time.strftime('%Y-%m-%d %H:%M:%S', sd))
            id=data['id']
            print ("id :%s" %data["id"])
            s=""
            for o in data["tag"]:s=s+str(o['tag_id'])+str(o['tag_name'])
            print s
            print ("sina:"+str(data["content"]))
            # self.restr.append(data["content"])
            self.restr.append([iam,createTime, id, country, asset, icontent])
            # self.restr.append([createTime,inid,icontent])dd
        return self.restr

    def walljsondata(self,i):
        if i is None:
            return
        self.restr = []
        j = i[i.find("(") + 1:i.rfind(")")]
        k= re.compile(r'\<\/?p\>').sub('', j)
        l = json.loads(k)["results"]

        #paixu
        l=sorted(l, key=lambda e: e.__getitem__('id'))
        if l:self.wnewid=l[-1]["id"]
        # for mt in l:
        #     self.wnewid = mt["id"]
        print "wnewid,wid",self.wnewid,self.wid
        if self.wnewid==self.wid:return
        self.restr = []
        print"l:",type(l)
        for m in l:
            createTime, id, country, asset, content =["","","","",""]
            id = m["id"]
            content = m["contentText"]
            createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(m["updatedAt"])))
            if self.wid<id:
                self.restr.append(["wscn",createTime, id, country, asset, content])
                print "write %s" %str(id)
                print content
                # createTime, important, country, asset, content = data
        self.wid=self.wnewid
        return self.restr

    def runsina(self):
        self.sinaurl()
        stri = self.request()
        rstr=self.jsondata(stri)
        # excel arr
        return rstr

    def runwallstreetcn(self):
        self.wallstreetcnurl()
        stri = self.request()
        # excel import stri
        rstr=self.walljsondata(stri)
        return rstr

    def getSpeech(self,text):
        # x=urllib.urlencode(text)
        url = 'http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd='+str(self.spd)+'&text='
        return url + str(text)

    def audioplay(self,text):
        subprocess.call(["mplayer", self.getSpeech(text)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__=="__main__":
    t = sina()
    n=nlp.nlpc()
    e=excelsave.excelsavec()
    t.spd=6
    t.setid(600367)
    xi=0
    while 1:
        t.restr=[]
        if xi==0:
            xi=1
            t.runsina()
        else:
            xi=0
            t.runwallstreetcn()
        k=[]
        if type(t.restr)!=str:
            k=t.restr
            k=n.startArr(k)
            e.saveAll(k)#写入excel
            e.eXsave()#保存

        for i in k:
            jbc=i
            #nlp tiqu key
            # jbc=str(i[4])
            # jbc=n.saveData(i)
            print "tip:",jbc
            # e.saveData(jbc)#写入excel
            t.audioplay(i[5])#语音 mplayer 播放 需要安装
            pass

        time.sleep(15)
