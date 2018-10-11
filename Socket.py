import socket
from time import sleep
from Settings import *


def openSocket():
    try:
        s = socket.socket()
        s.connect((HOST,PORT))
        s.send("PASS " + PASS + "\r\n")
        s.send("NICK " + IDENT + "\r\n")

        with open('joins.txt', 'a+') as jf:
            joins = jf.readlines()

        for chan in joins:
            s.send("JOIN #" + str(chan.strip()) + "\r\n")
            print "joined " + chan.strip()
            sleep(0.50)

        s.send("CAP REQ :twitch.tv/commands\r\n")

        return s

    except Exception, e:
        print "Opensocket error ", e

def sendChanMsg(s, chan, message):
    try:
        if chan.startswith("jtv"):
            chan = chan.split(",", 1)
            sleep(2)
            messageTemp = ("PRIVMSG #" + str(chan[0]) + " :/w " + chan[1] + " " + message)
        else:
            messageTemp = ("PRIVMSG #" + str(chan) + " :" + message)
        s.send(messageTemp.strip() + "\r\n")
        print "Sent message <{0}>".format(messageTemp)
    except Exception, e:
        print "sendmessage error ", e

