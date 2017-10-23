# -*- coding: utf-8 -*-
from Api import getUptime
from random import randint
from Socket import sendChanMsg
import json

def handleMsg(s, dik, modstatus, chan, user, message):
    try:
        uloste, b = message.split(' ', 1)
        b = b.strip()
    except:
        uloste = message.strip()
        b = ""
    try:
        modonlycmd = 0
        uloste = str(uloste)
        if chan.startswith("jtv"):
            uloste = dik["jtv"][uloste.lower().decode('utf8')]
        else:
            uloste = dik[chan][uloste.lower().decode('utf8')]
        if uloste != None:
            if '$user$' in uloste:
                uloste = uloste.replace('$user$', user)

            if '$mod$' in uloste:
                uloste = uloste.replace('$mod$', "")
                modonlycmd = 1

            if '$uptime$' in uloste:
                uloste = uloste.replace('$uptime$', getUptime(chan))

            if '$random100$' in uloste:
                uloste = uloste.replace('$random100$', str(randint(0, 100)))

            if '$d20$' in uloste:
                uloste = uloste.replace('$d20$', str(randint(1, 20)))

            if '$d6$' in uloste:
                uloste = uloste.replace('$d6$', str(randint(1, 6)))
                # this last so !paikal $random100$ doesnt work

            if '$own$' in uloste:
                uloste = uloste.replace('$own$', b)

            if not modonlycmd:
                sendChanMsg(s, chan, uloste)
            elif modonlycmd:
                modonlycmd = 0
                if modstatus and uloste != "":
                    sendChanMsg(s, chan, uloste)
    except Exception, e:
        #print "handlemsg error:", e
        pass

def delcom(s, dik, chan, user, message):
    try:
        if chan.startswith("jtv"):
            cmds = dik["jtv"]
        else:
            cmds = dik[chan]
        a, b = message.split('!delcom ', 1)
        #if b.startswith("!") == False:
        #    b = '!' + b
        poistettava = b.strip().lower().decode('utf8')

        action = cmds.get(poistettava)
        if action != None:
            del cmds[poistettava]
            dik.update(cmds)
            resp = "[DELETED]: " + poistettava + " : " + action
            if chan.startswith("jtv"):
                json.dump(cmds, open("jtvcommands", 'wb'), sort_keys=True, indent=3)
            else:
                json.dump(cmds, open(chan.strip() + "commands", 'wb'), sort_keys=True, indent=3)
            chan = "jtv," + user
            sendChanMsg(s, chan, resp)
    except Exception, e:
        print "delcom error:", e

def addcom(s, dik, chan, user, message):
    try:
        if chan.startswith("jtv"):
            cmds = dik["jtv"]
        else:
            cmds = dik[chan]
        a, b = message.split('!addcom ', 1)
        c, d = b.split(' ', 1)
        #if c.startswith("!") == False:
        #    c = '!' + c
        cmd = c.decode('utf8')
        if cmd.endswith(':'):
            cmd = cmd.replace(':', '')

        action = d.decode('utf8')
        action = action.strip().decode('utf8')
        cmd = cmd.strip().lower().decode('utf8')

        toAdd = {cmd: action}
        cmdDoesExist = cmds.get(cmd)
        if cmdDoesExist == None:
            cmds.update(toAdd)
            dik.update(cmds)
            if chan.startswith("jtv"):
                json.dump(cmds, open("jtvcommands", 'wb'), sort_keys=True, indent=3)
            else:
                json.dump(cmds, open(chan.strip() + "commands", 'wb'), sort_keys=True, indent=3)
            resp = "[ADDED]: " + cmd + " : " + action
            chan = "jtv," + user
            sendChanMsg(s, chan, resp)
        else:
            resp = cmd + " : " + cmdDoesExist + " already exists, please !delcom it first"
            chan = "jtv,"+user
            sendChanMsg(s, chan, resp)
    except Exception, e:
        print "addcom error:", e
