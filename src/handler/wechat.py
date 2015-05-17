import tornado.web
import tornado.gen
import hashlib
import urllib2
import json

from src.service.wechat import PostMsg,Wechat

class WechatHandler(tornado.web.RequestHandler):

    responseString = ""

    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        token = "gismanli"
        list=[token,timestamp,nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            self.write(echostr)

    def post(self):
        self.wechat = Wechat()
        self.responseMsg()
        self.write(self.responseString)

    def responseMsg(self):
        postStr = self.request.body

        if postStr:
            self.wechat.handle(postStr);
            replyMsg = self.wechat.getReplyMsg()
            self.responseString = replyMsg
        else:
            self.responseString = ""
