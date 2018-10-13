# -*- coding: utf-8 -*-
from Api import getUptime
from random import randint
from message_sending_service import sendingService
import json


def regular_commands(s, dik, modstatus, chan, user, message):
    try:
        output, own = message.split(' ', 1)
        own = own.strip()
    except:
        output = message.strip()
        own = ""
    try:
        modonlycmd = False
        output = str(output)
        if chan.startswith("jtv"):
            output = dik["jtv"][output.lower().decode('utf8')]
        else:
            output = dik[chan][output.lower().decode('utf8')]
        if output != None:
            if '$user$' in output:
                output = output.replace('$user$', user)

            if '$mod$' in output:
                output = output.replace('$mod$', "")
                modonlycmd = True

            if '$uptime$' in output:
                output = output.replace('$uptime$', getUptime(chan))

            if '$random100$' in output:
                output = output.replace('$random100$', str(randint(1, 100)))

            if '$d20$' in output:
                output = output.replace('$d20$', str(randint(1, 20)))

            if '$d6$' in output:
                output = output.replace('$d6$', str(randint(1, 6)))

            # this ($own$) last so !paikal $random100$ doesnt work
            if '$own$' in output:
                output = output.replace('$own$', own)

            if not modonlycmd:
                sendingService.send_msg(s, chan, output)
            elif modonlycmd:
                if modstatus and output != "":
                    sendingService.send_msg(s, chan, output)
    except Exception, e:
        pass


def delcom(s, dik, chan, user, message, splittext):
    try:
        if chan.startswith("jtv"):
            cmds = dik["jtv"]
        else:
            cmds = dik[chan]
        a, b = message.split(splittext, 1)

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
            sendingService.send_msg(s, chan, resp)
    except Exception, e:
        print "delcom error:", e


def addcom(s, dik, chan, user, message, splittext):
    try:
        if chan.startswith("jtv"):
            cmds = dik["jtv"]
        else:
            cmds = dik[chan]
        a, b = message.split(splittext, 1)
        c, d = b.split(' ', 1)

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
            sendingService.send_msg(s, chan, resp)
        else:
            resp = cmd + " : " + cmdDoesExist + " already exists, please !delcom it first"
            chan = "jtv," + user
            sendingService.send_msg(s, chan, resp)
    except Exception, e:
        print "addcom error:", e
