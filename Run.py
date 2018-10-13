#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import string
import sys
from multiprocessing import Pool, Queue
from threading import Thread
from time import sleep

from Api import getFollowStatus
from Init import joinRoom
from message_sending_service import sendingService
from hardcoded_commands import hardcoded_commands
from Read import getUser, getMessage, getChannel, getMod, getUserWhisper, getMessageWhisper, getUserID
from settings import OWNER
from Socket import openSocket
from regular_commands import regular_commands, addcom, delcom


class SocketHelper:
    def __init__(self):
        self.socket = None

    def set_socket(self, s):
        self.socket = s

    def get_socket(self):
        return self.socket

socketHelper = SocketHelper()


class CommandHelper():
    def __init__(self):
        self.dik = self.refresh_dik()

    def set_dik(self, dik):
        self.dik = dik

    def get_dik(self):
        return self.dik

    def renew_dik(self):
        self.dik = self.refresh_dik()

    @staticmethod
    def refresh_dik():
        with open("joins.txt", 'a+') as joinsfile:
            joins = joinsfile.readlines()

        cmddict = {}

        for i in range(len(joins)):
            cmddict.update({joins[i].strip() : ""})
            filepath = joins[i].strip()+"commands"

            if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                cmddict2 = {  joins[i].strip() : json.load( open( filepath, "a+" ) )  }
            else:
                defaultdik = { "!defaultcmd" : "defaultaction" }
                json.dump( defaultdik, open(filepath, "a+") )
                cmddict2 = {joins[i].strip() : json.load(open(filepath, "a+") )}

            cmddict.update(cmddict2)

        return cmddict
        
cmds = CommandHelper()


def parse_info(args):
    s = socketHelper.get_socket()
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
            userid = getUserID(msg)
            if user == OWNER:
                modstatus = True
            return userid, user, message, chan, modstatus

        if "WHISPER" in msg:
            user = getUserWhisper(msg).strip().lower()
            message = getMessageWhisper(msg).strip()
            chan = "jtv," + user
            userid = getUserID(msg)
            return userid, user, message, chan, True


def message_actions(messageQueue):
    s = socketHelper.get_socket()
    Thread(target=message_limit_handler).start()
    kuismafix = ["strongkuisma", "harshmouse", "teukka"]
    while True:
        (userid, user, message, chan, modstatus, dik) = messageQueue.get()
        Thread(target=regular_commands, args=(s, dik, modstatus, chan, user, message,)).start()
        Thread(target=hardcoded_commands, args=(s, chan, user, modstatus, message,)).start()

        if "has won the giveaway" in message and user == "nightbot":
            try:
                search, b = message.split(" ", 1)
                sendingService.send_msg(s, chan, getFollowStatus(search, chan))
            except Exception, e:
                print "nightbot giveaway detection error:", e

        if message.startswith("!kuismafix") and (modstatus or user == OWNER):
            try:
                if chan not in kuismafix:
                    kuismafix.append(chan)
                    sendingService.send_msg(s, chan, "Channel has been kuismafixed")
                elif chan in kuismafix:
                    kuismafix.remove(chan)
                    sendingService.send_msg(s, chan, "Kuismafix has been lifted")
            except Exception, e:
                print "kuismafix error:", e

        if message.startswith("!addcom ") or message.startswith("lisääkomento "):
            try:
                if modstatus:
                    if message.startswith("!addcom "):
                        splittext = "!addcom "
                    if message.startswith("lisääkomento"):
                        splittext = "lisääkomento "
                    if chan in kuismafix and user != OWNER and splittext == "!addcom ":
                        print "addcom skipped"
                    else:
                        addcom(s, dik, chan, user, message, splittext)
                        cmds.renew_dik()
            except Exception, e:
                print "error at !addcom ", e

        if message.startswith("!delcom ") or message.startswith("poistakomento "):
            try:
                if modstatus:
                    if message.startswith("poistakomento"):
                        splittext = "poistakomento "
                    if message.startswith("!delcom "):
                        splittext = "!delcom "
                    if chan in kuismafix and user != OWNER and splittext == "!delcom ":
                        print "delcom skipped"
                    else:
                        delcom(s, dik, chan, user, message, splittext)
                        cmds.renew_dik()
            except Exception, e:
                print "error at !delcom ", e

        if message.startswith("!editcom ") or message.startswith("muutakomento "):
            try:
                if modstatus:
                    if message.startswith("muutakomento"):
                        splittext = "muutakomento "
                    if message.startswith("!editcom "):
                        splittext = "!editcom "
                    if chan in kuismafix and user != OWNER and splittext == "!editcom ":
                        print "editcom skipped"
                    else:
                        todel = message.split(" ", 2)
                        delcom(s, dik, chan, user, ("!delcom " + todel[1]), "!delcom ")
                        addcom(s, dik, chan, user, message.replace(splittext, "!addcom ", 1), "!addcom ")
                        cmds.renew_dik()
            except Exception, e:
                print "error @!editcom ", e


def message_limit_handler():
    while 1:
        sendingService.add_messages_left(1)
        sleep(1.5)


def main_loop():
    s = socketHelper.get_socket()
    incoming_pool = Pool(1)
    joinRoom(s)
    s.send("CAP REQ :twitch.tv/tags\n")
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sendingService.send_msg(s, OWNER, "started")
    msg_q = Queue()

    th = Thread(target=message_actions, args=(msg_q,))
    th.daemon = True
    th.start()
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
        templines = list()
        for i in xrange(len(temp)):
            pack = (temp[i])
            templines.append(pack)
        
        msg_arr = incoming_pool.map(parse_info, templines)
        for resp in msg_arr:
            if resp != None:
                resp_list = list(resp)
                resp_list.append(cmds.get_dik())
                msg_q.put(resp_list)


if __name__ == '__main__':
    while 1:
        try:
            if socketHelper.get_socket() is not None:
                socketHelper.get_socket().close()
        except:
            pass
        socketHelper.set_socket(openSocket())
        try:
            print "Starting..."
            main_loop()
        except Exception, e:
            print "highest level program error: ", e
            pass
