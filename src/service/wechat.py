# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
import re
import json

from tornado.util import import_object
from xml.etree import ElementTree as ET

class PostMsg(object):
    fromUsername = ""
    toUsername = ""
    createTime =  ""
    msgType = ""
    content = ""
    msgId = ""
    scale = ""
    label = ""
    title = ""
    description = ""
    url = ""
    event = ""
    eventKey = ""

class ReplyMsg(object):
    toUserName = ""
    fromUserName = ""
    createTime = ""
    msgType = ""
    content = ""
    musicUrl = ""
    hQMusicUrl = ""
    articleCount = ""
    articles = list()
    articles

class Wechat(object):
    postMsg = None
    replyMsg = None

    def __init__(self):
        self.replyMsg = ReplyMsg()

    def handle(self, postStr):
        self.postMsg = self._postMsgParse(postStr)
        if self.postMsg:
            self._myMsgHandle()

    def _myMsgHandle(self):
        if self.postMsg.msgType == 'text':
            command = self.postMsg.content.strip()
            req = urllib2.Request("http://www.tuling123.com/openapi/api?key=873ba8257f7835dfc537090fa4120d14&info=" + command)
            data = json.loads(urllib2.urlopen(req).read())
            if 'url' in data:
                content = data['text'] + '\n' + data['url']
            else:
                content = data['text']
            regex = re.sub(u'图灵机器人',u'饥渴的机器人',content)
            regex = re.sub(';','\n',regex)
            self.replyMsg = self._makeExceptionReplyMsg(regex)
            return
        elif self.postMsg.msgType == 'event':
            content = "欢迎关注本微信，这个微信是本人业余爱好所建立，也是想一边学习Python一边玩的东西，直接回复即可聊天。"
            self.replyMsg = self._makeExceptionReplyMsg(content)

    def _postMsgParse(self,postStr):
        postObj = ET.fromstring(postStr)
        postMsg = None
        try:
            postMsg = PostMsg()
            fromUsername = postObj.find("FromUserName").text
            postMsg.fromUsername = fromUsername

            toUsername = postObj.find("ToUserName").text
            postMsg.toUsername = toUsername

            createTime = postObj.find("CreateTime").text
            postMsg.createTime = createTime

            msgType = postObj.find("MsgType").text
            postMsg.msgType = msgType
            msgId = postObj.find("MsgId").text
            postMsg.msgId = msgId

            if msgType == 'text':
                content = postObj.find("Content").text
                content = content.encode('utf-8')
                postMsg.content = content

            elif msgType =='event':
                postMsg.event = "gismanli"
            else:
                print msgType
        except Exception, e:
            print e

        return postMsg

    def _makeExceptionReplyMsg(self,exception_msg):
        replyMsg = ReplyMsg()
        replyMsg.toUsername = self.postMsg.fromUsername
        replyMsg.fromUsername = self.postMsg.toUsername
        replyMsg.createTime = str(int(time.time()))
        replyMsg.msgType = 'text'
        replyMsg.content = exception_msg
        return replyMsg

    def _makeTextReplyMsg(self):

        textTpl = "<xml>\n\
                    <ToUserName><![CDATA[%s]]></ToUserName>\n\
                    <FromUserName><![CDATA[%s]]></FromUserName>\n\
                    <CreateTime>%s</CreateTime>\n\
                    <MsgType><![CDATA[%s]]></MsgType>\n\
                    <Content><![CDATA[%s]]></Content>\n\
                    <FuncFlag>0</FuncFlag>\n\
                    </xml>"
        resultStr = textTpl % (self.replyMsg.toUsername,
                                self.replyMsg.fromUsername,
                                self.replyMsg.createTime,
                                self.replyMsg.msgType,
                                self.replyMsg.content)

        return resultStr

    def getReplyMsg(self):
        replyMsgStr = ""
        if self.replyMsg:
            if self.replyMsg.msgType == 'text':
                replyMsgStr = self._makeTextReplyMsg()
            elif self.replyMsg.msgType == 'event':
                replyMsgStr = self._makeTextReplyMsg()
            else:
                print( "未知类型：%s" % self.replyMsg.msgType)
        else:
            error_msg = (self.config.get('exception','missing') % self.postMsg.content)
            self.replyMsg = self._makeExceptionReplyMsg(error_msg)
            replyMsgStr = self._makeTextReplyMsg()

        return replyMsgStr
