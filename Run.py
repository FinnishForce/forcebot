#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import sys
from multiprocessing import Pool, Queue
from threading import Thread
from time import sleep

from api import get_follow_status
from command_helper import cmds
from hardcoded_commands import hardcoded_commands
from init import joinRoom
from message_sending_service import sendingService
from read import get_user, get_message, get_channel, get_mod, get_user_id
from regular_commands import regular_commands, addcom, delcom
from settings import OWNER
from socket_helper import socketHelper


def parse_info(args):
    s = socketHelper.get_socket()
    #print s
    msg = args
    if "PING" in msg:
        print "PINGPONG"
        s.send("PONG :tmi.twitch.tv\r\n")
    else:
        user = get_user(msg).strip().lower()
        message = get_message(msg).strip()
        chan = get_channel(msg).strip().lower()
        modstatus = get_mod(msg)
        userid = get_user_id(msg)
        if user == OWNER:
            modstatus = True
        return userid, user, message, chan, modstatus



def message_actions(message_queue):
    s = socketHelper.get_socket()
    Thread(target=message_limit_handler).start()
    kuismafix = ["strongkuisma", "harshmouse", "teukka"]
    while True:
        (userid, user, message, chan, modstatus, dik) = message_queue.get()
        Thread(target=regular_commands, args=(s, dik, modstatus, chan, user, message,)).start()
        Thread(target=hardcoded_commands, args=(s, chan, user, modstatus, message,)).start()

        if "has won the giveaway" in message and user == "nightbot":
            try:
                search, b = message.split(" ", 1)
                sendingService.send_msg(s, chan, get_follow_status(search, chan))
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
                        cmds.renew()
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
                        cmds.renew()
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
                        cmds.renew()
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
                resp_list.append(cmds.get())
                msg_q.put(resp_list)


if __name__ == '__main__':
    while 1:
        try:
            if socketHelper.get_socket() is not None:
                socketHelper.get_socket().close()
        except:
            pass
        socketHelper.open_socket()
        try:
            print "Starting..."
            main_loop()
        except Exception, e:
            print "highest level program error: ", e
            pass
