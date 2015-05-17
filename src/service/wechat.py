# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
import re

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
            value = {'info':command}
            req = urllib2.Request("http://www.tuling123.com/openapi/productexp.do", urllib.urlencode(value))
            req.add_header('Cookie','JSESSIONID=aaa2rUy-Qesubf2DLcH1u; pgv_pvi=8508344320; pgv_si=s2071941120; CNZZDATA1000214860=1465977645-1431848223-%7C1432849191')
            xml = ET.fromstring(urllib2.urlopen(req).read())
            content = xml.find("Content")
            if content != None:
                regex = re.sub('图灵','',content.text)
                regex = re.sub('[<>]','',regex)
                regex = re.sub('[机器人]','饥渴的机器人',regex)
                self.replyMsg = self._makeExceptionReplyMsg(regex)
            else:
                content = "本屌不才，您不要问我这个，我在鸟不拉屎星，听不懂您说的是哪里..."
                self.replyMsg = self._makeExceptionReplyMsg(content)
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
