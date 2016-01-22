import string

def getUser(line):
   try:
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user
   except:
	print "Getuser error"

def getMessage(line):
   try:
	separate = line.split(":", 2)
	message = separate[2]
	return message
   except:
	print "Getmessage error"

def getChannel(line):
   try:
	separate = line.split("PRIVMSG #", 1)
	sep2 = separate[1].split(" :", 1)
	channel = sep2[0]
	return channel
   except:
	print "getchannel error"
