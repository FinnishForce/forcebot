import socket
from time import sleep
from Settings import *


class MessageSendingService:
    def __init__(self):
        print "message sending service inited"
        self.messagesLeft = 20

    def getMessagesLeft(self):
        return self.messagesLeft

    def addMessagesLeft(self, num):
        if self.messagesLeft < 20:
            self.messagesLeft += num

    def reduceMessagesLeft(self, num):
        if self.messagesLeft > 0:
            self.messagesLeft -= num

    def sendChanMsg(self, s, chan, message):
        try:
            print "messages left", self.messagesLeft
            while self.messagesLeft < 2:
                sleep(1)
            if chan.startswith("jtv"):
                chan = chan.split(",", 1)
                messageTemp = ("PRIVMSG #" + str(chan[0]) + " :/w " + chan[1] + " " + message)
            else:
                messageTemp = ("PRIVMSG #" + str(chan) + " :" + message)
            s.send(messageTemp.strip() + "\r\n")
            print "Sent message <{0}>".format(messageTemp)
            self.reduceMessagesLeft(1)
        except Exception, e:
            print "sendmessage error ", e


sendingService = MessageSendingService()
