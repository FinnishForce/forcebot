def getUser(line):
    try:
        separate = line.split(".tmi.twitch.tv PRIVMSG #")
        user = separate[0].split("@", 4)
        user = user[2]
        return user
    except Exception, e:
        print "Getuser error ->", e


def getUserWhisper(line):
    try:
        separate = line.split(".tmi.twitch.tv WHISPER ")
        user = separate[0].split("@", 4)
        user = user[2]
        return user.strip().lower()
    except Exception, e:
        print "Getuser error ->", e


def getMessage(line):
   try:
        separate = line.split(".tmi.twitch.tv PRIVMSG #")
        message = separate[1].split(" :", 1)
        message = message[1]
        print "message is <{0}>".format(message)
        return message
   except Exception, e:
        print "Getmessage error ->", e


def getMessageWhisper(line):
   try:
        separate = line.split(".tmi.twitch.tv WHISPER ")
        message = separate[1].split(" :", 1)
        message = message[1]
        return message
   except Exception, e:
        print "Getmessage error ->", e


def getChannel(line):
    try:
        separate = line.split("PRIVMSG #", 1)
        sep2 = separate[1].split(" :", 1)
        channel = sep2[0]
        return channel
    except Exception, e:
        print "getchannel error ->", e


def getMod(line):
    try:
        if "mod=0" in line:
            return False
        elif "mod=1" in line:
            return True
        else:
            print "this shouldn't happen (getmod)"
    except Exception, e:
        print "getmod error ->", e
