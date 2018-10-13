from time import sleep


class MessageSendingService:
    def __init__(self):
        print "message sending service inited"
        self.message_cap = 50
        self.messages_left = self.message_cap

    def get_messages_left(self):
        return self.messages_left

    def add_messages_left(self, num):
        if self.messages_left < self.message_cap:
            self.messages_left += num

    def reduce_messages_left(self, num):
        print "reducing messages"
        if self.messages_left > 0:
            self.messages_left -= num

    def send_msg(self, s, chan, message):
        try:
            print "messages left", self.messages_left
            while self.messages_left < 2:
                sleep(1)
            if chan.startswith("jtv"):
                chan = chan.split(",", 1)
                message_temp = ("PRIVMSG #" + str(chan[0]) + " :/w " + chan[1] + " " + message)
            else:
                message_temp = ("PRIVMSG #" + str(chan) + " :" + message)
            s.send(message_temp.strip() + "\r\n")
            print "Sent message <{0}>".format(message_temp)
            self.reduce_messages_left(1)
        except Exception, e:
            print "sendmessage error ", e


sendingService = MessageSendingService()
