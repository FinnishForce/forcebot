#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string
import json
from multiprocessing import Pool, Queue, Process
from threading import Thread
from time import sleep
from MessageSendingService import sendingService
from Read import getUser, getMessage, getChannel, getMod, getUserWhisper, getMessageWhisper
from Socket import openSocket
from Init import joinRoom
from Settings import OWNER
from Messagecommands import tryCommands
from Api import *
from handleMsg import handleMsg, addcom, delcom


class SocketHelper:
    def __init__(self):
        self.socket = None
    def setSocket(self, s):
        self.socket = s
    def getSocket(self):
        return self.socket

socketHelper = SocketHelper()


def refreshCmds():
    with open("joins.txt", 'a+') as joinsfile:
        joins = joinsfile.readlines()

    dik = {}

    for i in range(len(joins)):
        dik.update({joins[i].strip() : ""})
        filepath = joins[i].strip()+"commands"

        if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
            dik2 = {  joins[i].strip() : json.load( open( filepath, "a+" ) )  }
        else:
            defaultdik = { "!defaultcmd" : "defaultaction" }
            json.dump( defaultdik, open(filepath, "a+") )
            dik2 = {joins[i].strip() : json.load(open(filepath, "a+") )}

        dik.update(dik2)

    return dik


def parseInfo(args):
    s = socketHelper.getSocket()
    #print s
    msg = args
    if "PING" in msg:
        print "PINGPONG"
        s.send("PONG :tmi.twitch.tv\r\n")
    else:
        if "PRIVMSG" in msg:
            user = getUser(msg).strip().lower()
            message = getMessage(msg).strip()
            chan = getChannel(msg).strip().lower()
            modstatus = getMod(msg)
            if user == OWNER:
                modstatus = True
            return user, message, chan, modstatus

        if "WHISPER" in msg:
            user = getUserWhisper(msg).strip().lower()
            message = getMessageWhisper(msg).strip()
            chan = "jtv," + user
            return user, message, chan, True


def messageActions(messageQueue):
    s = socketHelper.getSocket()
    Thread(target=messageLimitHandler).start()
    kuismafix = ["strongkuisma", "harshmouse", "teukka"]
    while True:
        (user, message, chan, modstatus, dik) = messageQueue.get()
        Thread(target=handleMsg, args=(s, dik, modstatus, chan, user, message,)).start()
        Thread(target=tryCommands, args=(s, chan, user, modstatus, message,)).start()

        if "has won the giveaway" in message and user == "nightbot":
            try:
                search, b = message.split(" ", 1)
                sendingService.sendChanMsg(s, chan, getFollowStatus(search, chan))
            except Exception, e:
                print "nightbot giveaway detection error:", e

        if message.startswith("!kuismafix") and (modstatus or user == OWNER):
            try:
                if chan not in kuismafix:
                    kuismafix.append(chan)
                    sendingService.sendChanMsg(s, chan, "Channel has been kuismafixed")
                elif chan in kuismafix:
                    kuismafix.remove(chan)
                    sendingService.sendChanMsg(s, chan, "Kuismafix has been lifted")
            except Exception, e:
                print "kuismafix error:", e

        if message.startswith("!addcom ") and modstatus:
            try:
                if chan in kuismafix and (user != OWNER):
                    print "addcom skipped"
                else:
                    addcom(s, dik, chan, user, message)
            except Exception, e:
                print "error at !addcom ", e

        if message.startswith("!delcom ") and modstatus:
            try:
                if chan in kuismafix and user != OWNER:
                    print "delcom skipped"
                else:
                    delcom(s, dik, chan, user, message)
            except Exception, e:
                print "error at !delcom ", e

        if message.startswith("!editcom ") and modstatus:
            try:
                if chan in kuismafix and (user != OWNER):
                    print "editcom skipped"
                else:
                    todel = message.split(" ", 2)
                    delcom(s, dik, chan, user, ("!delcom " + todel[1]))
                    addcom(s, dik, chan, user, message.replace("!editcom", "!addcom", 1))
            except Exception, e:
                print "error @!editcom ", e


def messageLimitHandler():
    while 1:
        sendingService.addMessagesLeft(1)
        sleep(1.5)


def mainLoop():
    s = socketHelper.getSocket()
    incomingPool = Pool(1)
    joinRoom(s)
    s.send("CAP REQ :twitch.tv/tags\n")
    dik = refreshCmds()
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sendingService.sendChanMsg(s, OWNER, "started")
    msgQ = Queue()

    Process(target=messageActions, args=(msgQ,)).start()

    # Start looping
    while 1:
        temp = ""
        try:
            getit = s.recv(4096)
            # If we receive data with length of 0, we are disconnected. Try to reconnect when that happens.
            if len(getit) == 0:
                print "Disconnected..."
                break
            # print getit
            temp = filter(None, string.split(getit.encode("utf-8"), "\r\n"))
        except Exception, e:
            print "socket recv? error: ", e
            break
        sendingService.messagesLeft -= 1
        templines = list()
        for i in xrange(len(temp)):
            pack = (temp[i])
            templines.append(pack)

        msgArr = incomingPool.map(parseInfo, templines)
        for resp in msgArr:
            if resp != None:
                respList = list(resp)
                respList.append(dik)
                msgQ.put(respList)


if __name__ == '__main__':
    while 1:
        try:
            if socketHelper.getSocket() != None:
                socketHelper.getSocket().close()
        except:
            pass
        socketHelper.setSocket(openSocket())
        try:
            print "Starting..."
            mainLoop()
        except Exception, e:
            print "highest level program error: ", e
            pass
