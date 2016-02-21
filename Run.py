# -*- coding: utf-8 -*-
from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil


import json
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
from Api import *

def writePidFile():
  with open('my_pid', 'w') as f:
    f.write(str(os.getpid()))

def readQuitFile():
  with open('quited', 'r') as f:
    prevchan = f.readline()
  return prevchan

def refreshCmds():
  with open("joins.txt", 'a+') as joinsfile:
    joins = joinsfile.readlines()

  dik = {}
  if 1 == 1:
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
  #except Exception, e:
    #print e
  else:
    print "swag"
  return dik



def main_loop():
            
        
        s = openSocket()
        joinRoom(s)
        s.setblocking(0)
    #try:
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
        pogchamp = 0
        pogchamptimer = 0
        modonlycmd = 0
                
        dik = refreshCmds()
#	json.dump(dik, open("testfile.txt", "wb"))
#	json.dump(dik.get("finnishforce_"), open("test2file.txt", "wb"))
#	json.dump(dik.get("tuolijakkara"), open("test3file.txt", "wb"))
        writePidFile()
        prevchan = readQuitFile()
        sendChanMsg(s, prevchan, "Started MingLee")
#	print dik.get("susihukka2551")        
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
                                                        sleep(0.01)
                                except Exception, e:
                                        print "error ping "
					print e
                
                                       

                if temp != "":
                        if "PRIVMSG" in getit:
                          
                            cmds = dik.get(chan)
                            if modstatus == 'ok' or user == chan or user in approved:
                              modstatus = 'ok'

                            if message.startswith("!addcom ") and modstatus == "ok":
                              try:
                                a, b = message.split('!addcom ', 1)
                                c, d = b.split(' ', 1)
                                if c.startswith("!") == False:
                                    c = '!' + c
                                cmd = c.decode('utf8')
                                if cmd.endswith(':'):
                                    cmd = cmd.replace(':', '')
                                    sendChanMsg(s, chan, "commandi lisättiin oikein, mutta enää ei tarvitse käyttää kaksoispisteitä commandin addaamiseen. check !commands for more info about this change")

                                action = d.decode('utf8')
                                action = action.strip().decode('utf8')
                                cmd = cmd.strip().lower().decode('utf8')
                                
                                toAdd = {cmd : action}
                                cmdDoesExist = cmds.get(cmd)
                                if cmdDoesExist == None:
                                  cmds.update(toAdd)
                                  dik.update(cmds)
                                  json.dump(cmds, open(chan.strip()+"commands", 'wb'), sort_keys=True, indent=3)
                                  dik = refreshCmds()
                                  
                                  resp = "[ADDED]: " + cmd + " : " + action
                                  sendChanMsg(s, chan, resp)
                                  toLog = user + " "  + resp
                                  log(toLog, chan+"reports")
                                else:
                                  resp = cmd + " : " + cmdDoesExist + " already exists, please !delcom it first"
                                  sendChanMsg(s, chan, resp)
                              except Exception, e:
                                print "addcom error "
				print e
                                log("addcom error", "globalerror")

                            if message.startswith("!delcom ") and modstatus == "ok":
                              try:
                                a, b = message.split('!delcom ', 1)
                                if b.startswith("!") == False:
                                  b = '!' + b
                                poistettava = b.strip().lower().decode('utf8')

                                
                                action = cmds.get(poistettava)
                                if action != None:
                                  del cmds[poistettava]
                                  dik.update(cmds)
                                  resp = "[DELETED]: " + poistettava + " : " + action
                                  json.dump(cmds, open(chan.strip()+"commands", 'wb'), sort_keys=True, indent=3)
                                  dik = refreshCmds()
                                  sendChanMsg(s, chan, resp)
                                  toLog = user + " "  + resp
                                  log(toLog, chan+"reports")
                              except Exception, e:
                                print "delcom error "
				print e
                                log("delcom error", "globalerror")
                            
                            #if "pogchamp" in message.lower():
                            #    pogchamp = pogchamp + 1
                            #    pogchamptimer = timer()
                            #    if pogchamp >= 4:
                            #      pogchamp = 0
                            #      sendChanMsg(s, chan, "PogChamp ?")
              
                            if message == "!disablebot" and (user == chan or user == owner):
                                try:
                                    bannedrooms.append(chan)
                                    sendChanMsg(s, chan, "Bot has been disabled.")
                                except Exception, e:
                                    print "weird disable/enable bot error "
				    print e
                                
                            if message == "!enablebot" and (user == chan or user == owner):
                                try:
                                    bannedrooms.remove(chan)
                                    sendChanMsg(s, chan, "Bot has been enabled.")
                                except Exception, e:
                                    print "weird disable/enable bot error "
				    print e 
                            
                            if message.startswith("!discom") and (modstatus == 'ok') :
                                try:
                                    pamp = message.split("!discom ")
                                    banthis = chan + str(pamp[1])
                                    bannedcmds.append(banthis)
                                    resp = pamp[1] + " has been disabled."
                                    sendChanMsg(s, chan, resp)
                                except Exception, e:
                                    print "weird disable/enable command error "
				    print e
                                
                            if message.startswith("!encom") and (modstatus == 'ok'):
                                try:
                                    pamp = message.split("!encom ")
                                    unbanthis = chan + str(pamp[1])
                                    bannedcmds.remove(unbanthis)
                                    resp = pamp[1] + " has been enabled."
                                    sendChanMsg(s, chan, resp)
                                except Exception, e:
                                    print "weird disable/enable com error "
				    print e
                            
                            checkban = chan + message
                            if (user not in bannedusers) and (chan not in bannedrooms) and (checkban not in cooldownlist) and (checkban not in bannedcmds):
                                    if (checkban not in cooldownlist) and (message.startswith('!')):
                                        if ( len(cooldownlist) >= 1 ) :
                                          cooldownlist.pop(0)
                                    
                                        cdtimer = timer()
                                        cooldownlist.append(checkban)
                                        
                                    if message.startswith('!'):
                                      
                                      try:
                                        uloste, b = message.split(' ', 1)
                                        b = b.strip()
                                      except:
                                        uloste = message.strip()
                                        b = ""
                                      try:  
                                        uloste = str(uloste)
                                        uloste = cmds.get(uloste.lower().decode('utf8'))
                                        if uloste != None:
                                          if '$user$' in uloste:
                                            uloste = uloste.replace('$user$', user)
                                        
                                          if '$mod$' in uloste:
                                              uloste = uloste.replace('$mod$', "")
                                              modonlycmd = 1

                                          if '$uptime$' in uloste:
                                              uloste = uloste.replace('$uptime$', getUptime(chan))
                                          if '$random100$' in uloste:
                                              uloste = uloste.replace('$random100$', str( randint(0, 100) ) )
                                          if '$d20$' in uloste:
                                              uloste = uloste.replace('$d20$', str( randint(1, 20) ) )
                                          if '$d6$' in uloste:
                                              uloste = uloste.replace('$d6$', str( randint(1, 6) ) )
                                                          #this last so !paikal $random100$ doesnt work
                                          if '$own$' in uloste:
                                              uloste = uloste.replace('$own$', b)

                                          if modonlycmd == 0:
                                            sendChanMsg(s, chan, uloste) 
                                          elif modonlycmd == 1:
                                            modonlycmd = 0
                                            if modstatus == 'ok' and uloste != "":
                                              sendChanMsg(s, chan, uloste)
                                      except Exception, e:
                                           print e
                                      Process(target=tryCommands, args=(s, chan, user, modstatus, message)).start()
                            
                end = timer()
                elapsed = elapsed + (end-start)
                if(elapsed >= 300):
                        s.send("PONG :tmi.twitch.tv\r\n")
                        elapsed = 0

                if(end - cdtimer > 15):
                        if ( len(cooldownlist) >= 1):
                                cooldownlist.pop(0)

                #if(end - pogchamptimer > 15):
                #  pogchamp = 0
    #except Exception, e:
	#print e

if __name__ == '__main__':
    while 1:
        try:
                print "mainloop"
                main_loop()
        except Exception, e:
		main_loop()
                print "error in mainloop "
                print e
		#pass
               # main_loop()
                
