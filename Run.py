#!/usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing import Process
import os
import sys
import string
from Read import getUser, getMessage, getChannel, getMod, getUserWhisper, getMessageWhisper
from Socket import openSocket, sendChanMsg
from Init import joinRoom
from Messagecommands import tryCommands
from Api import *
from handleMsg import handleMsg, addcom, delcom

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


def main_loop():
    s = openSocket()
    joinRoom(s)
    s.setblocking(0)

    chan = ""
    user = ""
    modstatus = False
    message = ""
    s.send("CAP REQ :twitch.tv/tags\n")
    readbuffer = ""
    approved = [OWNER, 'mmorz', 'bulftrik']
    cdlist = []
    kuismafix = ["strongkuisma", "harshmouse"]

    dik = refreshCmds()
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sendChanMsg(s, OWNER, "started")

    # Start looping
    while 1:
        temp = ""
        try:
            getit = s.recv(4096)
            readbuffer = readbuffer + getit
            temp = string.split(readbuffer, "\r\n")
            readbuffer = temp.pop()
        except Exception, e:
            pass

        if temp != "":
            for line in temp:
                try:
                    if "PING" in line:
                        s.send("PONG :tmi.twitch.tv\r\n")
                    else:
                        if "PRIVMSG" in getit:
                            user = getUser(line).encode('utf8').strip().lower()
                            message = getMessage(line).encode('utf8').strip()
                            chan = getChannel(line).encode('utf8').strip().lower()
                            modstatus = getMod(line)


                        if "WHISPER" in getit:
                            user = getUserWhisper(line).encode('utf8').strip().lower()
                            message = getMessageWhisper(line).encode('utf8').strip()
                            chan = "jtv," + user
                            modstatus = False
                            if user == OWNER:
                                modstatus = True
                except Exception, e:
                    print "Error in 'for line in temp' ->", e

        if temp != "" and message != "" and ('PRIVMSG' or 'WHISPER' in getit) and not getit.startswith('PING :tmi.twitch.tv'):

            if modstatus or user == chan or user in approved:
                modstatus = True

            # Check if message is a command
            Process(target=handleMsg, args=(s, dik, modstatus, chan, user, message,)).start()
            Process(target=tryCommands, args=(s, chan, user, modstatus, message,)).start()

            if "has won the giveaway" in message and user == "nightbot":
                try:
                    search, b = message.split(" ", 1)
                    sendChanMsg(s, chan, getFollowStatus(search, chan))
                except Exception, e:
                    print "nightbot giveaway detection error:", e

            if message.startswith("!kuismafix") and (modstatus or user == OWNER):
                try:
                    if chan not in kuismafix:
                        kuismafix.append(chan)
                        sendChanMsg(s, chan, "Channel has been kuismafixed")
                    elif chan in kuismafix:
                        kuismafix.remove(chan)
                        sendChanMsg(s, chan, "Kuismafix has been lifted")
                except Exception, e:
                    print "kuismafix error:", e

            if message.startswith("!request ") and modstatus:
                try:
                    lista = dik[chan].get("!lista")

                    if lista is None:
                        lista = ""

                    toAppend = message.split("!request")[1].strip()

                    lista += toAppend + ", "

                    dik[chan].update({"!lista": lista})
                    dik.update(dik[chan])
                    json.dump(dik[chan], open(chan.strip() + "commands", 'wb'), sort_keys=True, indent=3)
                    cdlist.append(user)
                    sendChanMsg(s, chan, lista)

                except Exception, e:
                    print e

            if message.startswith("!delreq") and modstatus:
                try:
                    delnum = 1
                    try:
                        delnum = int(message.split("!delreq ")[1])
                    except:
                        pass
                    lista = dik[chan].get("!lista")
                    lista = lista.split(", ")
                    lista.pop(delnum-1)
                    lista = ", ".join(lista)
                    dik[chan].update({"!lista": lista})
                    dik.update(dik[chan])
                    json.dump(dik[chan], open(chan.strip() + "commands", 'wb'), sort_keys=True, indent=3)
                    sendChanMsg(s, chan, lista)
                except Exception, e:
                    print e
                    pass

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

            # After doing everything, reset message, user, channel etc
            message = ""
            user = ""
            chan = ""
            temp = ""
            readbuffer = ""
            getit = ""


if __name__ == '__main__':
    while 1:
        try:
            print "Starting..."
            main_loop()
        except Exception, e:
            print "mainloop error: ", e
            pass

