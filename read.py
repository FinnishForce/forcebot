def get_user(line):
    try:
        if ".tmi.twitch.tv PRIVMSG #" in line:
            separate = line.split(".tmi.twitch.tv PRIVMSG #")
        elif ".tmi.twitch.tv WHISPER " in line:
            separate = line.split(".tmi.twitch.tv WHISPER ")
        else:
            return ""
        user = separate[0].split("@", 4)
        user = user[2]
        return user
    except Exception, e:
        print "Getuser error ->", e


def get_user_id(line):
    try:
        separate = line.split(";")
        for snip in separate:
            if snip.startswith("user-id="):
                return snip.split("=")[1]
        return 0
    except Exception, e:
        print "getuserid error ->", e


def get_message(line):
    try:
        if ".tmi.twitch.tv PRIVMSG #" in line:
            separate = line.split(".tmi.twitch.tv PRIVMSG #")
        elif ".tmi.twitch.tv WHISPER " in line:
            separate = line.split(".tmi.twitch.tv WHISPER ")
        else:
            return ""
        message = separate[1].split(" :", 1)
        message = message[1]
        print "message is <{0}>".format(message)
        return message

    except Exception, e:
        print "Getmessage error ->", e


def get_channel(line):
    try:
        if ".tmi.twitch.tv PRIVMSG #" in line:
            separate = line.split("PRIVMSG #", 1)
        elif ".tmi.twitch.tv WHISPER " in line:
            return "jtv,"+get_user(line)
        else:
            return ""

        sep2 = separate[1].split(" :", 1)
        channel = sep2[0]
        return channel
    except Exception, e:
        print "getchannel error ->", e


def get_mod(line):
    try:
        if ".tmi.twitch.tv PRIVMSG #" in line:
            if "mod=0" in line:
                return False
            elif "mod=1" in line:
                return True
        elif ".tmi.twitch.tv WHISPER " in line:
            return False
        else:
            return False

    except Exception, e:
        print "getmod error ->", e
