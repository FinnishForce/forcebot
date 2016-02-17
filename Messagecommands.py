# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil
import signal

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
    from time import sleep, time
    from datetime import datetime, timedelta
    from Init import joinRoom
    from Logger import log
    from Settings import kaisanetacc, kaisanetpass, ftpserver
	
    num = 0
    addc = 0
    ismod = 0
    delc = 0
    exists = 0
    worked = 0
    approved = [owner, 'mmorz', 'bulftrik']
    
    delthis = ""
    chancmds = chan + 'commands.txt'
    with open(chancmds, 'a+') as cmdfile:
        commands = cmdfile.readlines()
    chanmods = chan + 'mods.txt'
	

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
            
    if message == "!bonus":
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
            random = randint(0, (vieweramount-1) )
            chosenone = viewerlist[random]
            
            resp = "Random viewer from list: " + chosenone.strip()
            sendChanMsg(s, chan, resp)
            resp2 = "/timeout " + chosenone.strip() + " 10"
            sendChanMsg(s, chan, resp2)

        except:
            print "Error random viewer"
            toLog = "error randomviewer"
            log(toLog, "globalerror")
            
    if message.startswith("!restartbot"):
        try:
          if (user == owner) or (modstatus == 'ok') or (user == chan):
            writeQuitFile(chan)
            killthis = readPidFile()
            killthis = int(killthis)
            os.kill(killthis, 15)
            subprocess.call(["cd /path/to/bot"], shell=True)
            subprocess.call(["sudo python Run.py"], shell=True)
        except:
            print "softreseterror"
            
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
            joinhere = user
            resp = ("joined #" + joinhere)
            sendChanMsg(s, chan, resp)

            joinChan(s, joinhere)                                                
        except:
            print "botjoin error"
            log("error botjoin", "globalerror")

    if message.startswith("!botquit"):
        try:
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

    if message.startswith("!delcom"):
        try:
            with open(chancmds, 'a+') as cmdfile:
                num = 0
                pois1 = 0
                pois2 = 0
                if modstatus == "ok":
                        a, b = message.split('!delcom ', 1)
                        if b.startswith("!") == False:
                            b = '!' + b
                        poistettava = b.strip().lower()
                        for sueless in commands:
                            if commands[num].strip().lower() == poistettava:
                                    delthis = commands[num+2]
                            num = num + 1


                        for linja in fileinput.input(chancmds, inplace=True):
                            if (poistettava == linja.strip().lower()) and pois1 == 0:
                                    pois1 = 1
                                    continue
                            print linja,
                        fileinput.close()

                        delthis = delthis.strip().lower()
                        for linja2 in fileinput.input(chancmds, inplace=True):
                            if (delthis == linja2.strip().lower()) and pois2 == 0:
                                    pois2 = 1
                                    continue
                            print linja2,

                        fileinput.close()

                        if pois1 == 1 and pois2 == 1:
                          if chan == "susihukka2551":
                              cmdfile.close()
                              session = ftplib.FTP(ftpserver, kaisanetacc, kaisanetpass)
                              file = open('susihukka2551commands.txt', 'rb')
                              session.storbinary('STOR susihukka2551commands.txt', file)
                              file.close()
                              session.quit()
                          toLog = user + " deleted command " + poistettava + " , action: " + delthis
                          resp = "deleted " + poistettava + " : " + delthis
                          info = chan + "reports"
                          log(toLog, info)
                          sendChanMsg(s, chan, resp)
        except:
            print "delcom error"
            log("error delcom", "globalerror")

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



    if message.startswith("!addcom"):
        with open(chancmds, 'a+') as cmdfile:
                if modstatus == "ok":
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
			cmd = cmd.strip().lower()
			action = action.strip().lower()
                        for sueless in commands:
                            if commands[addc].strip().lower().decode('utf8') == cmd:
                                response = ("Command already exists " + commands[addc].strip() + " = " + commands[addc+2].strip() + " please !delcom " + commands[addc].strip() + " first")
                                exists = 1
                                sendChanMsg(s, chan, response)
                            if commands[addc].strip().lower().decode('utf8') == action:
                                response = ("Same action already exists in command " + commands[addc-2].strip() + " = " + commands[addc].strip() + " please !delcom " + commands[addc-2].strip() + " first")
                                exists = 1
                                sendChanMsg(s, chan, response)
                            addc = addc + 1
                                
                        if action.startswith("!"):
                                action = action.replace('!', '')
                                
                        if exists != 1:
                                cmdfile.write('\n'.encode('utf8') + cmd.encode('utf8') + '\n\n'.encode('utf8') + action.encode('utf8') + '\n'.encode('utf8'))
                                toLog = user + " added command " + cmd + " that does action: " + action
                                resp = "added " + cmd + " : " + action
                                sendChanMsg(s, chan, resp)
                                info = chan + "reports"
                                log(toLog, info)
                                if chan.strip() == "susihukka2551":
                                    cmdfile.close()
                                    session = ftplib.FTP(ftpserver, kaisanetacc, kaisanetpass)
                                    file = open('susihukka2551commands.txt', 'rb')
                                    session.storbinary('STOR susihukka2551commands.txt', file)
                                    file.close()
                                    session.quit()
                    except:
                        print "error"
                        log("error addcom", "globalerror")

    if message.startswith('!'):
        num = 0
        worked = 0
        modonlycmd = 0
        try:
            a, b = message.split(' ', 1)
            b = b.strip()
            worked = 1
        except:
            a = ""
            b = ""
            worked = 0

        for sueless in commands:
            if commands[num].strip().lower() == message.strip().lower():
                uloste = commands[num+2]

                if '$user$' in uloste:
                    uloste = uloste.replace('$user$', user)
                if '$own$' in uloste:
                    uloste = uloste.replace('$own$', b)
                if '$mod$' in uloste:
                    uloste = uloste.replace('$mod$', "")
                    modonlycmd = 1
                    if modstatus == 'ok':
                        sendChanMsg(s, chan, uloste)
			break
                    else:
                        print "someone tried to use onlymod command"

                if '$uptime$' in uloste:
                    uloste = uloste.replace('$uptime$', getUptime(chan))
                if '$random100$' in uloste:
                    uloste = uloste.replace('$random100$', str( randint(0, 100) ) )
                if '$d20$' in uloste:
                    uloste = uloste.replace('$d20$', str( randint(1, 20) ) )
                if '$d6$' in uloste:
                    uloste = uloste.replace('$d6$', str( randint(1, 6) ) )
                  
                    
                if modonlycmd != 1: 
                    sendChanMsg(s, chan, uloste)
                    break
	    
	    num = num + 1
            #if commands[num].strip().lower() == a.strip().lower():
            #    if worked == 1:
            #        uloste = commands[num+2].strip()
            #        if '$user$' in uloste:
            #            uloste = uloste.replace('$user$', user)
            #        if '$own$' in uloste:
            #            uloste = uloste.replace('$own$', b)
            #        if '$mod$' in uloste:
            #            uloste = uloste.replace('$mod$', "")
            #            modonlycmd = 1
            #            if modstatus == "ok":
	    #		    print "action"
            #                sendChanMsg(s, chan, uloste)
            #            else:
            #                print "someone tried to use onlymod command"
            #        if '$uptime$' in uloste:
            #            uloste = uloste.replace('$uptime$', getUptime(chan))
            #        if '$random100$' in uloste:
            #            uloste = uloste.replace('$random100$', str( randint(0, 100) ) )
            #        if '$d20$' in uloste:
            #            uloste = uloste.replace('$d20$', str( randint(1, 20) ) )
            #        if '$d6$' in uloste:
            #            uloste = uloste.replace('$d6$', str( randint(1, 6) ) )
            #        
            #
            #        if modonlycmd != 1: 
            #                sendChanMsg(s, chan, uloste)
            #        break                                                        
	    #
            
