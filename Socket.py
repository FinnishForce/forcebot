import socket
import fileinput
from time import sleep
from Settings import *


MSGLIMIT = 100

def openSocket():
	try:
		s = socket.socket()
		s.connect((HOST,PORT))
		s.send("PASS " + PASS + "\r\n")
		s.send("NICK " + IDENT + "\r\n")
		chanjoins = 'joins.txt'
		with open(chanjoins, 'a+') as joinsfile:
			joins = joinsfile.readlines()

		for sueless in joins:
			s.send("JOIN #" + str(sueless.strip()) + "\r\n")
			print "joined " + sueless.strip()
			sleep(0.35)

		s.send("CAP REQ :twitch.tv/commands\r\n")

		return s
	except Exception, e:
		print "Opensocket error ", e

def sendMessage(s, message):
	try:
		messageTemp = "PRIVMSG #" + str(CHANNEL) + " :" + str(message)
		s.send(messageTemp + "\r\n")
	except:
		print "sendmessage error"

def sendChanMsg(s, chan, message):
	try:
		if chan.startswith("jtv"):
			chan = chan.split(",", 1)
			messageTemp = ("PRIVMSG #" + str(chan[0]) + " :/w " + chan[1] + " " + message)
		else:
			messageTemp = ("PRIVMSG #" + str(chan) + " :" + message)
		s.send(messageTemp.strip() + "\r\n")
	except Exception, e:
		print "sendmessage error ", e


def joinChan(s, chan):
	try:
		exists = 0
		addc = 0
		chanjoins = 'joins.txt'
		with open(chanjoins, 'a+') as joinsfile:
			joins = joinsfile.readlines()

		for somethings in joins:
			if joins[addc].strip().decode('utf8') == chan.decode('utf8'):
				exists = 1
			addc = addc + 1

			if exists != 1:
				joinsfile.write(chan.encode('utf8') + '\n'.encode('utf8'))

		s.send("JOIN #" + str(chan) + "\r\n")
	except Exception, e:
		print "joinchan error ", e

def quitChan(s, chan):
	try:
		s.send("PART #" + str(chan) + "\r\n")

		chanjoins = 'joins.txt'
		joinsfile = open(chanjoins, 'a+')
		joins = joinsfile.readlines()
		poistettava = chan.strip()

		for linja in fileinput.input(chanjoins, inplace=True):
			if poistettava.strip() == linja.strip():
				continue
			print linja,

		fileinput.close()

	except Exception, e:
		print "quitchan error ", e
