# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil
import signal
import pickle

def refreshCmds():
  with open("joins.txt", 'a+') as joinsfile:
    joins = joinsfile.readlines()

  dik = {}

  for i in range(len(joins)):
    dik.update({joins[i].strip() : ""})
    dik2 = {joins[i].strip() : json.load(open(joins[i].strip()+"commands", "r"))}
    dik.update(dik2)


from Api import *
from Socket import *
from Read import *

def readPidFile():
  with open('my_pid', 'r') as f:
        pid = f.read()
  return pid

def writeQuitFile(chan):
  with open('quited', 'w') as f:
        f.write(chan)

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def tryCommands(s, chan, user, modstatus, message):
    import os
    import subprocess
    import sys
    import ftplib
    import string
    import select
    import fileinput
    from timeit import default_timer as timer
    from time import sleep, time, mktime
    from datetime import datetime, timedelta
    from Init import joinRoom
    from Logger import log
    from Settings import kaisanetacc, kaisanetpass, ftpserver, IDENT, owner
        
    num = 0
    addc = 0
    ismod = 0
    delc = 0
    exists = 0
    worked = 0
    approved = [owner, 'mmorz', 'bulftrik']
    
    delthis = ""      

    if message.startswith('!amount '):
      try:
        
        try:
          a, lookup = message.split("!amount ")
        except:
          print "error"
          
        num = 0
        
        with open(chan+'log.txt', 'r') as searchFile:
	  first_line = searchFile.readlines()[2]
	  with open(chan+'log.txt', 'r') as file:
	   for line in file:
		if lookup.lower() in line.lower():
		  num = num + line.lower().count(lookup.lower())
          
          #first_line = searchFile.readlines()[2]
          timestring1, timestring2, b = first_line.split(' ', 2)
          timestring = timestring1 + " " + timestring2
          
          timestamp = datetime.now() - datetime.strptime(timestring, "%d-%m-%Y %H:%M:%S" )
          
	  timestamp, useless= str(timestamp).split('.')
	  t1, t2, t3 = timestamp.split(":")
	  timestamp = t1 + "h " + t2 + "m " + t3 + "s "
          resp =  str(lookup) + " count during last " + str(timestamp) + ": " + str(num)
          sendChanMsg(s, chan, resp)
      except Exception, e:
        print "!amount error"
        print e


    if message.startswith('!title'):
      try:
        try:
          a, thisChan = message.split("!title ")
        except:
          thisChan = chan

        title = getTitle(thisChan)
        resp = "[" + thisChan + "] " + title
        sendChanMsg( s, chan, resp )
      except Exception, e:
        print "!title error "
        print e
    
    if ("word1" and  "word2") in message:
      sendChanMsg(s, owner, message)
    
    if message.startswith('!modtest'):
        if modstatus =='"ok' or user == chan or user in approved:
            sendChanMsg(s, chan, "ok")
        else:
            sendChanMsg(s, chan, "fail")
            
    #print "hello i am " + str(os.getpid())

    try:
        totalrandom = randint(-500000, 500000)
        if (totalrandom == 87):
            msg = "/timeout " + user + " 87"
            toLog = "JACKPOT, " + user + " got pamp at #" + chan
            log(toLog, "jackpot")
            sendChanMsg(s, chan, msg)
            if modstatus == "ok":
                msg2 = user + " was lucky"
                ismod = 1
                                            
            if ismod == 0:
                 msg2 = user + " was unlucky and got timeouted for 87 seconds"
                 sendChanMsg(s, chan, msg2)
    except:
        log("random unluck error", "globalerror")

    if message.startswith("!pid"):
        try:
            resp = "Process id: " + str( os.getpid() )
            sendChanMsg( s, chan, resp )
        except:
            print "error pid"
    
    if message.startswith("!loltest"):
        try:
            a, splitted = message.split("!loltest ")
            
            try:
                name, server = splitted.split("s:")
                name = str(name).strip().lower()
                server = str(server).strip().lower()
            except:
                name = str(splitted).strip()
                server = "euw"

            summonerid = getLeagueSummonerId(server, name)
            summonerid = str(summonerid)
            resp = getLeagueLastGame(server, name, summonerid)
            sendChanMsg(s, chan, resp)
        except:
            print "lolid error"
            
    if message.startswith('!bonus'):
        try:
            sendChanMsg(s, chan, "PogChamp ?")
            sleep(2)
            sendChanMsg(s, chan, "BrokeBack")
        except:
            log("bonuserror", globalerror)
    
    if message.startswith("!wikipedia"):
        try:
            a, rest = message.split("!wikipedia ")
            try:
                title, lang = rest.split("lang:", 1)
                title = title.strip()
                lang = lang.strip()
            except:
                title = rest.strip()
                lang = "en"
            url, summary = getWikipediaUrl(title, lang)
            resp = url + " : " + summary
            sendChanMsg(s, chan, resp)
        except:
            print "wikipedia fake error"

    if message.startswith("!wiki"):
        try:
            a, rest = message.split("!wiki ")
            site, title = rest.split("-", 1)
            resp = getWikiaUrl(site.strip(), title.strip())
            sendChanMsg(s, chan, resp)
        except:
            log("error wiki", "globalerror")

    if message.startswith("!lolwiki"):
        try:
            a, title = message.split("!lolwiki")
            resp = getWikiaUrl("lolwiki", title.strip())
            sendChanMsg(s, chan, resp)
        except:
            log("error lolwiki", "globalerror")

    if message.startswith("!rswiki"):
        try:
            a, title = message.split("!rswiki")
            title = title.strip()
            resp = getWikiaUrl("rswiki", title)
            sendChanMsg(s, chan, resp)

        except:
            log("error rswiki", "globalerror")

    if message.startswith("!hswiki"):
        try:
            a, title = message.split("!hswiki")
            resp = getWikiaUrl("hswiki", title.strip())
            sendChanMsg(s, chan, resp)
        except:
            log("error hswiki", "globalerror")

            
    if message.startswith("!randomviewer"):
        try:
            viewerlist = []
            viewerlist, vieweramount = getViewers(chan)
	    try:
		viewerlist.remove(owner)
		viewerlist.remove(IDENT)
		vieweramount -= 2
	    except Exception, e:
		print "viewerlist remove error"
		print e
            chosenone = random.choice(viewerlist) #randint(0, (vieweramount-1) )
            #chosenone = viewerlist[random]
		
	    
            #print viewerlist, vieweramount
            viewers = ', '.join(viewerlist)


            chance = ( 1.0/float(vieweramount) ) * 100
            resp0 = "Viewers in raffle: " + str(vieweramount) + ", chance to get chosen: " + str( round(chance,5) ) + "%"
            sendChanMsg(s, chan, resp0)
            
            
            resp = "Random viewer from list: " + chosenone
            sendChanMsg(s, chan, resp)
            #resp2 = "/timeout " + chosenone.strip() + " 10"
            #sendChanMsg(s, chan, resp2)

        except Exception, e:
            print "Error random viewer"
	    print e
            toLog = "error randomviewer"
            log(toLog, "globalerror")
            
    if message.startswith("!restartbot"):
        try:
          if (user == owner) or (modstatus == 'ok') or (user == chan):
            writeQuitFile(chan)
            killthis = readPidFile()
            killthis = int(killthis)
            os.kill(killthis, 15)
            sendChanMsg(s, chan, "restarting...")
            subprocess.call(["cd /home/pi/Desktop/ForceBotti"], shell=True)
            subprocess.call(["sudo python Run.py"], shell=True)
        except Exception, e:
            print "softreseterror"
	    print e
            
    if message.startswith("!rng"):
        try:
            u, a = message.split("!rng ")
            print u, a
            a, b = a.split(" ")
            a = int(a)
            b = int(b)
            
            if a > b and b != 0:
                b = a*b
                a = b/a
                b = b/a
            elif a > b and b == 0:
                b = a
                a = 0
                
            r = randint(int(a), int(b))
            resp = "You got " + str(r) + " (" + str(int(a)) + "-" + str(int(b)) + ")"
            sendChanMsg(s, chan, resp)
        except:
            print "rng error"
            log("error rng", "globalerror")
    
    if message.startswith("!joinlobby"):
        try:
            resp = getJoin()
            sendChanMsg(s, chan, resp)
        except:
            print "!join error wot"
            log("error joinlobby", "globalerror")
    
    if message.startswith("!botjoin"):
        try:
          try:
            a, joinhere = message.split("!botjoin ")
          except:
            joinhere = user
            resp = ("joined #" + joinhere)
            sendChanMsg(s, chan, resp)

          joinChan(s, joinhere)                                                
        except:
            print "botjoin error"
            log("error botjoin", "globalerror")

    if message.startswith("!botquit"):
        try:
          try:
            a, quithere = message.split("!botquit ")
          except:
            quithere = user
            resp = ("leaving from #" + quithere + ", goodbye")
            sendChanMsg(s, chan, resp)
          quitChan(s, quithere)
        except:
            print "botquit error"
            log("error botquit", "globalerror")

    if message.startswith("!cpustats"):
        try:
            cpu_temperature = get_cpu_temperature()
            cpu_usage = psutil.cpu_percent()
            resp1 = "CPU usage: " + str(cpu_usage) + "%" + " | CPU temperature: " +  str(cpu_temperature) + "C"
            sendChanMsg(s, chan, resp1)

        except:
            log("cpustats error", "globalerror")


    if message.startswith("!killbot"):
        if (user == owner) or (user in approved):
            try:
                writeQuitFile(chan)
                sendChanMsg(s, chan, "riPepperonis bot, waking from dead in 1-2 min")
                restartbot()
            except:
                print "error in restartbotrun.py"
                log("error restartbot", "globalerror")
    
    if message.startswith("!pyramid"):
        try:
            if user == owner or user == chan:
                a, b = message.split('!pyramid')
                temp = b
                sendChanMsg(s, chan, temp)
                temp = b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b
                sendChanMsg(s, chan, temp)
                temp = b 
                sendChanMsg(s, chan, temp)
                sleep(0.1)
        except:
            print "pyramid error"
            log("error pyramid", "globalerror")

    if message.startswith("!updatemods"):
        try:
            updateMods(chan)
        except:
            print "updatemods error"
            log("error updatemods", "globalerror")

    if message.startswith("!adminspeak"):
        try:
            if user == owner:
                a, b = message.split('!adminspeak')
                b = b.strip()
                c, m = b.split(' ', 1)
                sendChanMsg(s, c, m)
        except:
            print "error adminspeak"
            log("error adminspeak", "globalerror")

    if message.startswith("!updatecommands"):
        try:
            session = ftplib.FTP(ftpserver, kaisanetacc, kaisanetpass)
            file = open('susihukka2551commands.txt', 'rb')
            session.storbinary('STOR susihukka2551commands.txt', file)
            file.close()
            session.quit()
        except:
            print "updatecommands error"
            log("error updatecommands", "globalerror")

    if message.startswith("!Laddcom") or message.startswith("!laddcom"):
        try:
            with open(chancmds, 'a+') as cmdfile:
                    if modstatus == "ok":
                        try:
                            a, b = message.split('m !', 1)
                            c, d = b.split(': ', 1)
                            c = '!' + c
                            cmd = c.decode('utf8')
                            action = d.decode('utf8')
                            cmd = cmd.strip().lower()
                            action = action.strip().lower()

                            for sueless in commands:
                                    if commands[addc].strip().lower().decode('utf8') == cmd:
                                            response = ("Command already exists " + commands[addc].strip() + " = " + commands[addc+2] + " please !delcom !" + commands[addc].strip() + "first")
                                            exists = 1
                                            sendChanMsg(s, chan, response)
                                            break
                                    
                                    if commands[addc].strip().lower().decode('utf8') == action:
                                            response = ("Same action already exists in command " + commands[addc-2].strip() + " = " + commands[addc] + " please !delcom !" + commands[addc-2].strip() + "first")
                                            exists = 1
                                            sendChanMsg(s, chan, response)
                                            break
                                    addc = addc + 1
                        
                            if action.startswith("!"):
                                    action = action.replace('!', '')
                                    
                            if exists != 1:
                                    cmdfile.write('\n'.encode('utf8') + cmd.encode('utf8') + '\n\n'.encode('utf8') + action.encode('utf8') + '\n'.encode('utf8'))
                                    toLog = user + " added command " + cmd + " that does action: " + action
                                    info = chan + "reports"
                                    resp = "added " + cmd + " : " + action
                                    sendChanMsg(s, chan, resp)
                                    log(toLog, info)
                                    if chan.strip() == "susihukka2551":
                                            cmdfile.close()
                                            session = ftplib.FTP(ftpserver, kaisanetacc, kaisanetpass)
                                            file = open('susihukka2551commands.txt', 'rb')
                                            session.storbinary('STOR susihukka2551commands.txt', file)
                                            file.close()
                                            session.quit()
                        except:
                            msg = "@" + user + " look now,> !addcom !test: test, muista kaksoispisteet ::::"
                            sendChanMsg(s, chan, msg)
        except:
            print "error in laddcom"
            log("error Laddcom", "globalerror")


    if message.startswith("!csfind"):
        try:
            a, b = message.split('!csfind')
            b = b.strip()
            b = str(b)
            if b.startswith("7656119"):
                resp = getSteamStats(b)
            else:
                b = convertToSteam64(b)
                resp = getSteamStats(b)

            sendChanMsg(s, chan, resp)
        except:
            print "error in csfind"
            log("error csfind", "globalerror")

    if message.startswith("!vac"):
        try:
            a, b = message.split('!vac')
            b = b.strip()
            b = str(b)
            if b.startswith("7656119"):
                resp = getPlayerBans(b)
            else:
                b = convertToSteam64(b)
                resp = getPlayerBans(b)

            sendChanMsg(s, chan, resp)
        except:
            print "error in vac"
            log("error vac", "globalerror")

    if message.startswith("!laststats"):
        try:
            resp = getSteamStats("76561198185015081")
            sendChanMsg(s, chan, resp)
        except:
            print "laststat error hapnd"
            log("error laststats", "globalerror")

    if message.startswith("!tussarikills"):
        try:      
            b = "76561198185015081"
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getTussariKills(b)
            else:
                b = convertToSteam64(b)
                resp = getTussariKills(b)

            sendChanMsg(s, chan, resp)
        except:
            print "tussarikill (hukka) error hapnd"
            log("error tussarikills", "globalerror")

    if message.startswith("!mytussarikills"):
        try:      
            a, b = message.split('!mytussarikills')
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getTussariKills(b)
            else:
                b = convertToSteam64(b)
                resp = getTussariKills(b)

            sendChanMsg(s, chan, resp)
        except:
            print "tussarikill (general) error hapnd"
            log("error mytussarikills", "globalerror")

    if message.startswith("!kills"):
        try:      
            a, wpn = message.split('!kills')
            b = "76561198185015081"
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getKills(b, wpn)
            else:
                b = convertToSteam64(b)
                resp = getKills(b, wpn)

            sendChanMsg(s, chan, resp)
        except:
            print "kills (hukka) error hapnd"
            log("error kills", "globalerror")

    if message.startswith("!mykills"):
        try:      
            a, b, wpn = message.split(' ')
            b = b.strip()
            b = str(b)
            wpn = wpn.strip()
            
            if b.startswith("7656119"):
                resp = getKills(b, wpn)
            else:
                b = convertToSteam64(b)
                resp = getKills(b, wpn)

            sendChanMsg(s, chan, resp)
        except:
            print "mykills error hapnd"
            log("error mykills", "globalerror")


    if message.startswith("!color "):
        try:
            a, b = message.split('!color')
            saythis = "/color " + b.strip()
            sendChanMsg(s, chan, saythis)
        except:
            log("error color", "globalerror")



