# -*- coding: utf-8 -*-
from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil

import threading
from multiprocessing import Process, Queue, current_process
import os
import sys
import ftplib
import string
import select
import fileinput
from timeit import default_timer as timer
from time import sleep, time
from datetime import datetime, timedelta
from Read import getUser, getMessage, getChannel, getMod
from Socket import openSocket, sendMessage, sendChanMsg, joinChan, quitChan, whisperSocket
from Init import joinRoom
from Logger import log
from Messagecommands import tryCommands
from Settings import *

def writePidFile():
  pid = str(os.getpid())
  f = open('my_pid', 'w')
  f.write(pid)
  f.close()

def readQuitFile():
  f = open('quited', 'r')
  prevchan = f.readline()
  f.close()
  return prevchan

def main_loop():
        
        
        s = openSocket()
        joinRoom(s)
        s.setblocking(0)
        
        chan = ""
        user = ""
        modstatus = ""
        message = ""
                
        s.send("CAP REQ :twitch.tv/tags\n")
        readbuffer = ""
        elapsed = 0
        end = 0
        bannedrooms = []
        cooldownlist = []
        bannedcmds = []
        bannedusers = ['bulfbot']
	approved = [owner, 'mmorz', 'bulftrik']

        cdtimer = 0

        
        writePidFile()
        prevchan = readQuitFile()
        
        sendChanMsg(s, prevchan, "Started MingLee")
        
        reload(sys)
        sys.setdefaultencoding("utf8")
        sendChanMsg(s, owner, "started")
        while 1:
                start = timer()
                temp = ""
                
                try:
                        getit = s.recv(4096)
                        readbuffer = readbuffer + getit
                        temp = string.split(readbuffer, "\n")
                        
                        readbuffer = temp.pop()
                except:
                        sleep(0.1)

                if temp != "":
                	for line in temp:
                                try:
                                        
                                        if "PING" in line:
                                                s.send("PONG :tmi.twitch.tv\r\n")
                                        else:
                                                if "PRIVMSG" in getit:
                                                        user = getUser(line).encode('utf8')
                                                        message = getMessage(line).encode('utf8')
                                                        chan = getChannel(line).encode('utf8')
                                                        modstatus = getMod(line).encode('utf8')
                                                        

                                                        user = user.strip()
                                                        message = message.strip()
                                                        chan = chan.strip()

                                                        user = user.lower()
                                                        chan = chan.lower()
                                                       
                                                        time = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
                                                        toLog = user.decode('utf-8') + ": " + message.decode('utf-8')
                                                        log(toLog, chan)
                                                else:
                                                        sleep(0.1)
                                except:
                                        print "error ping"
                
                                       

                if temp != "":
                        if "PRIVMSG" in getit:
                            
			    if modstatus == 'ok' or user == chan or user in approved:
				modstatus = 'ok'

                            if message == "!disablebot" and (user == chan or user == owner):
                                try:
                                    bannedrooms.append(chan)
                                    sendChanMsg(s, chan, "Bot has been disabled.")
                                except:
                                    print "weird disable/enable bot error"
                                
                            if message == "!enablebot" and (user == chan or user == owner):
                                try:
                                    bannedrooms.remove(chan)
                                    sendChanMsg(s, chan, "Bot has been enabled.")
                                except:
                                    print "weird disable/enable bot error"
                            
                            if message.startswith("!discom") and (modstatus == 'ok') :
                                try:
                                    pamp = message.split("!discom ")
                                    banthis = chan + str(pamp[1])
                                    bannedcmds.append(banthis)
                                    resp = pamp[1] + " has been disabled."
                                    sendChanMsg(s, chan, resp)
                                except:
                                    print "weird disable/enable command error"
                                
                            if message.startswith("!encom") and (modstatus == 'ok'):
                                try:
                                    pamp = message.split("!encom ")
                                    unbanthis = chan + str(pamp[1])
                                    bannedcmds.remove(unbanthis)
                                    resp = pamp[1] + " has been enabled."
                                    sendChanMsg(s, chan, resp)
                                except:
                                    print "weird disable/enable com error"
                            
                            checkban = chan + message
                            if (user not in bannedusers) and (chan not in bannedrooms) and (checkban not in cooldownlist) and (checkban not in bannedcmds):
                                    if (checkban not in cooldownlist) and (message.startswith('!')):
                                        if ( len(cooldownlist) >= 1 ) :
                                          cooldownlist.pop(0)
                                    
                                        cdtimer = timer()
                                        cooldownlist.append(checkban)
                                            
                                    Process(target=tryCommands, args=(s, chan, user, modstatus, message)).start()
                        
                end = timer()
                elapsed = elapsed + (end-start)
                if(elapsed >= 300):
                        s.send("PONG :tmi.twitch.tv\r\n")
                        elapsed = 0

		if(end - cdtimer > 15):
			if ( len(cooldownlist) >= 1):
				cooldownlist.pop(0)


if __name__ == '__main__':
    while 1:
        try:
                print "mainloop"
                main_loop()
        except:
                print "error in mainloop"
                main_loop()
                
