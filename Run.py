#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Vote import startVote, addVote, endVote
from Logger import log
from multiprocessing import Process
import os
import sys
import string
from time import strftime
from time import time as idiotclock
from Read import getUser, getMessage, getChannel, getMod, getUserWhisper, getMessageWhisper
from Socket import openSocket, sendMessage, sendChanMsg, joinChan, quitChan
from Init import joinRoom
from Messagecommands import tryCommands
from Api import *
from handleMsg import handleMsg, addcom, delcom

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
    msglog = {}
    s.send("CAP REQ :twitch.tv/tags\n")
    readbuffer = ""
    elapsed = 0
    elapsed2 = 0
    toldit = 0
    spam = 1
    adtime = 300
    checkban = ""
    prevline = ""
    votenum = 0
    done1, done2, done3 = 0,0,0
    choices = {}
    votes = {}
    voters = {}
    voteon = {}
    options = {}
    msglogfreq = 500
    prevtemp = ""
    approved = [owner, 'mmorz', 'bulftrik']
    cooldownlist = []
    cdlist = []
    cdtimer = 0
    modonlycmd = 0
    kuismafix = ["strongkuisma", "harshmouse"]
    gamerequs = {}

    dik = refreshCmds()
    writePidFile()
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sendChanMsg(s, owner, "started")
    while 1:
        start = idiotclock()
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
                            modstatus = getMod(line)

                            user = user.strip().lower()
                            message = message.strip()
                            chan = chan.strip().lower()
                            #time = datetime.now().strftime('%Y-%d-%m %H:%M:%S')


                        if "WHISPER" in getit:
                            user = getUserWhisper(line).encode('utf8')
                            message = getMessageWhisper(line).encode('utf8')
                            chan = "jtv," + user
                            modstatus = False
                            if user == "finnishforce_":
                                modstatus = True
			
			#msglog[chan].append(strftime('%x %X') + "<{0}>: {1}".format(user, message))
			#print msglog
		 
		except:
		   pass
		


	try:
	   msglog[chan]
	except:
	   msglog[chan] = ['']
	   pass
	
    	end = idiotclock()
        #elapsed = elapsed + (end-start)
        elapsed2 = elapsed2 + (end-start)
        #if(elapsed >= 300):
        #  s.send("PONG :tmi.twitch.tv\r\n")
        #  elapsed = 0
        
        if (elapsed2 >= 30):
	  try:
            cdlist.pop(0)
	    elapsed2 = 0
	  except:
	    pass
        
                
                    




        if (temp != "" and ("PRIVMSG" or "WHISPER" in getit) and checkban != (user+chan+message)):
            if modstatus or user == chan or user in approved:
                modstatus = True
            checkban = user + chan + message
	    msglog[chan].append(strftime('%x %X') + "<{0}>: {1}".format(user, message))
	    if len(msglog[chan]) > msglogfreq:
		log(msglog[chan], chan)
		del msglog[chan]
            if message.startswith(''):
                if ( len(cooldownlist) >= 1 ) :
                    cooldownlist.pop(0)
                try:
                    voteon[chan]
                except Exception, e:
		    pass
                    voteon[chan] = 0
                    voters[chan] = ['']

                #cdtimer = timer()
                cooldownlist.append(checkban)

                if message.startswith(''):
                    #handleMsg(s, dik, modstatus, chan, user, message)
                    #tryCommands(s, chan, user, modstatus, message)
		    
                    Process(target=handleMsg, args=(s, dik, modstatus, chan, user, message,)).start()
                    Process(target=tryCommands, args=(s, chan, user, modstatus, message,)).start()
                    #p1.start()
                    #p2.start()
		
		if "has won the giveaway" in message and user.lower() == "nightbot":
		    try:
			search, b = message.split(" ", 1)
			sendChanMsg(s, chan, getFollowStatus(search, chan))
		    except Exception, e:
			print "nightbot giveaway detection error:", e		

		if message.startswith("!freq") and user == owner:
		    try:
			a, b = message.split("!freq ")
			msglogfreq = int(b)
		    except Exception, e:
			print "logfreq error:", e
                if message.startswith("!kuismafix") and (modstatus or user==owner):
                    try:
                        if chan not in kuismafix:
                            kuismafix.append(chan)
                            sendChanMsg(s, chan, "Channel has been kuismafixed")
                        elif chan in kuismafix:
                            kuismafix.remove(chan)
                            sendChanMsg(s, chan, "Kuismafix has been lifted")
                    except Exception, e:
                        print "kuismafix error:", e
		
		if message.startswith("!request ") and user not in cdlist:
		    try:
			lista = dik[chan].get("!lista")
			if lista == None:
			  lista = ""
			#print lista
			toAppend = message.split("!request")[1].strip()
			#print toAppend
			lista += toAppend + ", "
			#print lista
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
		    except:
			pass

                if message.startswith("!startvote ") and voteon[chan] == 0 and modstatus:
                    try:
                        choices[chan], votes[chan] = startVote(message)
                        sendChanMsg(s, chan, "Vote started")
                        options[chan] = ("Options: " + str(", ".join(choices[chan])))
			#nr = 0
			#string = ""
                        #for i in choices[chan]:
			#	string = string + str(nr+1) + ". " + choices[chan][nr]
			#	nr = nr+1
			#options[chan] = string
			sendChanMsg(s, chan, str(options[chan]))
                        voteon[chan] = 1
                        print "choices:", choices

                    except Exception, e:
                        print "startvote error,", e

                if message.startswith("!options"):
                    try:
                        sendChanMsg(s, chan, str(options[chan]))
                    except:
                        pass

                #print "b4 vote:", voters, voteon[chan]

                if message.startswith("!vote ") and voteon[chan] == 1 and user not in voters[chan]:
                    try:

                        votes[chan] = addVote(choices[chan], votes[chan], message)
                        voters[chan].append(user)

                        #print votes[chan]
                        #print "voters:", voters[chan]

                        voter_amount = len(voters[chan])-1
                        #chan = "jtv,"+user
                        if voter_amount % 5 == 0:
                            sendChanMsg(s, chan, "{0} votes currently in".format(voter_amount))
                    except Exception, e:
                        print e

                if message.startswith("!endvote") and voteon[chan] == 1 and modstatus:
                    try:
                        sendChanMsg(s, chan, ("Most votes: "+endVote(choices[chan], votes[chan])))
                        voteon[chan] = 0
                        choices[chan] = ['']
                        votes[chan] = ['']
                        voters[chan] = ['']
                        options[chan] = ['']
                    except Exception, e:
                        print e

                if message.startswith("!addcom ") and modstatus:
                    try:
                        if chan in kuismafix and (user != owner):
                            print "addcom skipped"
                        else:
                            addcom(s, dik, chan, user, message)
                    except Exception, e:
                        print "error @!addcom ", e

                if message.startswith("!delcom ") and modstatus:
                    try:
                        if chan in kuismafix and user != owner:
                            print "delcom skipped"
                        else:
                            delcom(s, dik, chan, user, message)
                    except Exception, e:
                        print "error @!delcom ", e

                if message.startswith("!editcom ") and modstatus:
                    try:
                        if chan in kuismafix and (user != owner):
                            print "editcom skipped"
                        else:
                            todel = message.split(" ", 2)
                            delcom(s, dik, chan, user, ("!delcom " + todel[1]))
                            addcom(s, dik, chan, user, message.replace("!editcom", "!addcom", 1))
                    except Exception, e:
                        print "error @!editcom ", e


#                end = timer()
#                elapsed = elapsed + (end-start)
#                elapsed2 = elapsed2 + (end-start)
#		print elapsed2
#                if(elapsed >= 300):
#                    s.send("PONG :tmi.twitch.tv\r\n")
#                    elapsed = 0#
#		done1, done2, done3 = 0, 0, 0
#		try:
#		 if (elapsed2 >= 18 and done1 != 1):
#		    print elapsed2, dik["susihukka2551"]["!casinot"]
#		    done1 = 1
#		    sendChanMsg(s, "susihukka2551", dik["susihukka2551"]["!casinot"])
#		 if (elapsed2 >= 36 and done2 != 1):
#		    done2 = 1
#		    sendChanMsg(s, "susihukka2551", dik["susihukka2551"]["!casinot2"])
#		 if (elapsed2 >= 54):
#		    sendChanMsg(s, "susihukka2551", dik["susihukka2551"]["!casinot3"])
#		    done1, done2 = 0, 0
#		    elapsed2 = 0
#		except Exception, e:
#		 print "hukkamainos error", e
#		 pass
#               if(end - cdtimer > 15):
#                      if ( len(cooldownlist) >= 1):
#                             cooldownlist.pop(0)


if __name__ == '__main__':
    while 1:
        try:
            print "mainloop"
            main_loop()
        except Exception, e:
            print "mainloop error: ", e
	    log([str(e)], "error")
            pass

