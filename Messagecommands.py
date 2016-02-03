# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil

from Api import *

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def tryCommands(s, chan, user, message):
    import os
    import sys
    import ftplib
    import string
    import select
    import fileinput
    from timeit import default_timer as timer
    from time import sleep, time
    from datetime import datetime, timedelta
    from Read import getUser, getMessage, getChannel
    from Socket import openSocket, sendMessage, sendChanMsg, joinChan, quitChan
    from Init import joinRoom
    from Logger import log
    num = 0
    addc = 0
    lastchan = ""
    ismod = 0
    delc = 0
    exists = 0
    worked = 0
    kaisanetacc = 'sue'
    kaisanetpass = 'less'
    delthis = ""
    chancmds = chan + 'commands.txt'
    with open(chancmds, 'a+') as cmdfile:
        commands = cmdfile.readlines()
    chanmods = chan + 'mods.txt'
    with open(chanmods, 'a+') as modsfile:
        mods = modsfile.readlines()

    try:
        totalrandom = randint(-5000, 5000)
        log(str(totalrandom), "random")
        if (totalrandom == 87):
            msg = "/timeout " + user + " 87"
            toLog = "JACKPOT, " + user + " got pamp"
            log(toLog, "unluckyusers")
            sendChanMsg(s, chan, msg)
            sleep(0.2)
            with open(chanmods, 'a+') as modsfile:
                 mods = modsfile.readlines()
            for names in mods:
                if names.strip().lower() == user.strip().lower():
                    msg2 = user + " was lucky"
                    ismod = 1
                                            
            if ismod == 0:
                 msg2 = user + " was unlucky and got timeouted for 87 seconds"
                 sendChanMsg(s, chan, msg2)
    except:
        log("random unluck error", "globalerror")


    if message.startswith("!randomviewer"):
        try:
            if chan != lastchan:
                viewerlist = []
                viewerlist = getViewers(chan)
                vieweramount = getViewerAmount(chan)
            random = randint(0, (vieweramount-1) )
            chosenone = viewerlist[random]
            
            resp = "Random viewer from list: " + chosenone
            
            sendChanMsg(s, chan, resp)
            sleep(0.2)
            resp2 = "/timeout " + chosenone.strip() + " 10"
            sendChanMsg(s, chan, resp2)
            lasttime = timer()
            lastchan = chan

        except:
            print "Error random viewer"
            toLog = "error randomviewer"
            log(toLog, "globalerror")
            

    if message.startswith("!rng"):
        try:
            u, a = message.split("!rng ")
            print u, a
            a, b = a.split(" ")
            r = randint(int(a), int(b))
            resp = "You got " + str(r)
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
            joinhere = user.strip()
            joinChan(s, joinhere)                                                
        except:
            print "botjoin error"
            log("error botjoin", "globalerror")

    if message.startswith("!botquit"):
        try:
            quithere = user.strip()
            resp = ("leaving from channel #" + quithere + ", goodbye")
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


    if message.startswith("!restartbot"):
        for modnames in mods:
            if modnames.strip().lower() == user.strip().lower() or user.strip() == "finnishforce_":
                try:
                    sendChanMsg(s, chan, "restarting bot, brb 1-2 min")
                    restartbot()
                except:
                    print "error in restartbotrun.py"
                    log("error restartbot", "globalerror")
                    
    if message.startswith("!uptime"):
        try:
            uptime = getUptime(chan)
            msg = chan + " has been online for " + uptime
            sendChanMsg(s, chan, msg)
        except:
            log("uptime error", "globalerror")

    if message.startswith("!pyramid"):
        try:
            if user.strip() == "finnishforce_" or user.strip() == chan.strip():
                a, b = message.split('!pyramid')
                temp = b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
                temp = b+b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
                temp = b+b+b+b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
                temp = b+b
                sendChanMsg(s, chan, temp)
                sleep(0.1)
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
            if user == "finnishforce_":
                a, b = message.split('!adminspeak')
                b = b.strip()
                c, m = b.split(' ', 1)
                sendChanMsg(s, c, m)
        except:
            print "error adminspeak"
            log("error adminspeak", "globalerror")

    if message.startswith("!updatecommands"):
        try:
            session = ftplib.FTP('ftp.kaisanet.net', kaisanetacc, kaisanetpass)
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
                for names in mods:
                    if names.strip().lower() == user.strip().lower():
                        try:
                            a, b = message.split('m !', 1)
                            c, d = b.split(': ', 1)
                            c = '!' + c
                            cmd = c.decode('utf8')
                            action = d.decode('utf8')

                            for sueless in commands:
                                    if commands[addc].strip().lower().decode('utf8') == cmd.strip().lower():
                                            response = ("Command already exists " + commands[addc].strip() + " = " + commands[addc+2] + " please !delcom !" + commands[addc].strip() + "first")
                                            exists = 1
                                            sendChanMsg(s, chan, response)
                                            break
                                    
                                    if commands[addc].strip().lower().decode('utf8') == action.strip().lower():
                                            response = ("Same action already exists in command " + commands[addc-2].strip() + " = " + commands[addc] + " please !delcom !" + commands[addc-2].strip() + "first")
                                            exists = 1
                                            sendChanMsg(s, chan, response)
                                            break
                                    addc = addc + 1
                        
                            if action.startswith("!"):
                                    action = action.replace('!', '')
                                    
                            if exists != 1:
                                    cmdfile.write('\n'.encode('utf8') + cmd.encode('utf8') + '\n\n'.encode('utf8') + action.encode('utf8') + '\n'.encode('utf8'))
                                    toLog = user + " added command " + cmd + " that does action: " + action.strip()
                                    info = chan + "reports"
                                    resp = "added " + cmd.strip() + " : " + action.strip()
                                    sendChanMsg(s, chan, resp)
                                    log(toLog, info)
                                    if chan.strip() == "susihukka2551":
                                            cmdfile.close()
                                            session = ftplib.FTP('ftp.kaisanet.net', kaisanetacc, kaisanetpass)
                                            file = open('susihukka2551commands.txt', 'rb')
                                            session.storbinary('STOR susihukka2551commands.txt', file)
                                            file.close()
                                            session.quit()
                                    break
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
                for names in mods:
                    if names.strip().lower() == user.strip().lower():
                        a, b = message.split('!delcom ', 1)
                        poistettava = b.strip()
                        for sueless in commands:
                            if commands[num].strip().lower() == poistettava.strip().lower():
                                    delthis = commands[num+2]
                            num = num + 1


                        for linja in fileinput.input(chancmds, inplace=True):
                            if (poistettava.strip().lower() == linja.strip().lower()) and pois1 == 0:
                                    pois1 = 1
                                    continue
                            print linja,
                        fileinput.close()

                        delthis = delthis.strip()
                        for linja2 in fileinput.input(chancmds, inplace=True):
                            if (delthis.strip().lower() == linja2.strip().lower()) and pois2 == 0:
                                    pois2 = 1
                                    continue
                            print linja2,

                        fileinput.close()
                
                        if chan.strip() == "susihukka2551":
                            cmdfile.close()
                            session = ftplib.FTP('ftp.kaisanet.net', kaisanetacc, kaisanetpass)
                            file = open('susihukka2551commands.txt', 'rb')
                            session.storbinary('STOR susihukka2551commands.txt', file)
                            file.close()
                            session.quit()
                        if pois1 == 1 and pois2 == 1:
                            toLog = user + " deleted command " + poistettava + " that did action: " + delthis.strip()
                            info = chan + "reports"
                            log(toLog, info)
                            resp = "deleted " + poistettava.strip() + " : " + delthis.strip()
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
            for names in mods:
                if names.strip().lower() == user.strip().lower():
                    try:
                        a, b = message.split('!addcom ', 1)
                        c, d = b.split(' ', 1)
                        if c.startswith("!") == False:
                            c = '!' + c
                        #c = '!' + c # this is useless after fixing bug
                        cmd = c.decode('utf8')
                        if cmd.endswith(':'):
                            cmd = cmd.replace(':', '')
                            sendChanMsg(s, chan, "commandi lisättiin oikein, mutta enää ei tarvitse käyttää kaksoispisteitä commandin addaamiseen. check !commands for more info about this change")

                        action = d.decode('utf8')

                        for sueless in commands:
                            if commands[addc].strip().lower().decode('utf8') == cmd.strip().lower():
                                response = ("Command already exists " + commands[addc].strip() + " = " + commands[addc+2].strip() + " please !delcom " + commands[addc].strip() + " first")
                                exists = 1
                                sendChanMsg(s, chan, response)
                                break
                                
                            if commands[addc].strip().lower().decode('utf8') == action.strip().lower():
                                response = ("Same action already exists in command " + commands[addc-2].strip() + " = " + commands[addc].strip() + " please !delcom " + commands[addc-2].strip() + " first")
                                exists = 1
                                sendChanMsg(s, chan, response)
                                break
                            addc = addc + 1
                                
                        if action.startswith("!"):
                                action = action.replace('!', '')
                                
                        if exists != 1:
                                cmdfile.write('\n'.encode('utf8') + cmd.encode('utf8') + '\n\n'.encode('utf8') + action.encode('utf8') + '\n'.encode('utf8'))
                                toLog = user + " added command " + cmd + " that does action: " + action.strip()
                                resp = "added " + cmd + " : " + action
                                sendChanMsg(s, chan, resp)
                                info = chan + "reports"
                                log(toLog, info)
                                if chan.strip() == "susihukka2551":
                                    cmdfile.close()
                                    session = ftplib.FTP('ftp.kaisanet.net', kaisanetacc, kaisanetpass)
                                    file = open('susihukka2551commands.txt', 'rb')
                                    session.storbinary('STOR susihukka2551commands.txt', file)
                                    file.close()
                                    session.quit()
                                break
                    except:
                        print "error"
                        log("error addcom", "globalerror")


    if message.startswith("!addmod"):
        with open(chanmods, 'a+') as modsfile:
            for names in mods:
                if names.strip().lower() == user.strip().lower():
                    try:
                        a, b = message.split('!addmod', 1)
                        b = b.strip()
                        for sueless in mods:
                            if mods[addc].strip().decode('utf8') == b.decode('utf8'):
                                response = ("Mod is already on list")
                                exists = 1
                                sendChanMsg(s, chan, response)
                                break
                            addc = addc + 1
                                
                        if exists != 1:
                            modsfile.write('\n'.encode('utf8') + b.encode('utf8') + '\n'.encode('utf8'))
                            toLog = user + " added mod " + b
                            info = chan + "reports"
                            log(toLog, info)
                            break
                    except:
                        msg = "@" + user + "check commands how to use !addmod or error was happeneds,,"
                        sendChanMsg(s, chan, msg)
                        break
    
    if message.startswith("!delmod"):
        with open(chanmods, 'a+') as modsfile:
            num = 0
            if chan.strip().lower() == user.strip().lower():
                try:
                    a, b = message.split('!delmod ', 1)
                    poistettava = b.strip()
                    for sueless in commands:
                        if commands[num].strip() == poistettava.strip():
                                delthis = commands[num+2]
                        num = num + 1

                    for linja in fileinput.input(chanmods, inplace=True):
                        if poistettava.strip() == linja.strip():
                            continue
                        print linja,
                    fileinput.close()

                    delthis = delthis.strip()
                    for linja2 in fileinput.input(chanmods, inplace=True):
                        if delthis.strip() == linja2.strip():
                            continue
                        print linja2,

                    fileinput.close()

                    toLog = user + " deleted mod " + b
                    info = chan + "reports"
                    log(toLog, info)
                except:
                    print "error in !delmod"
                    log("error delmod", "globalerror")


    #for songs in sr:
        #if message.startswith(songs):
            #sendChanMsg(s, "finnishforce_", "found")


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
                    for names in mods:
                            if names.strip().lower() == user.strip().lower():
                                    sendChanMsg(s, chan, uloste)
                            else:
                                    print "someone tried to use onlymod command"
                if '$uptime$' in uloste:
                    uloste = uloste.replace('$uptime$', getUptime(chan))
                    
                if modonlycmd != 1: 
                    sendChanMsg(s, chan, uloste)
                    break

            if commands[num].strip().lower() == a.strip().lower():
                if worked == 1:
                    uloste = commands[num+2].strip()
                    if '$user$' in uloste:
                        uloste = uloste.replace('$user$', user)
                    if '$own$' in uloste:
                        uloste = uloste.replace('$own$', b)
                    if '$mod$' in uloste:
                        uloste = uloste.replace('$mod$', "")
                        modonlycmd = 1
                        for names in mods:
                            if names.strip().lower() == user.strip().lower():
                                sendChanMsg(s, chan, uloste)
                            else:
                                print "someone tried to use onlymod command"
                    if '$uptime$' in uloste:
                        uloste = uloste.replace('$uptime$', getUptime(chan))

                    if modonlycmd != 1: 
                            sendChanMsg(s, chan, uloste)
                    sleep(0.1)
                    break                                                        

            num = num + 1
