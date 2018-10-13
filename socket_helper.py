import socket
from time import sleep
from settings import HOST, PORT, PASS, IDENT


class SocketHelper(object):
    def __init__(self):
        self.socket = None

    def set_socket(self, s):
        self.socket = s

    def get_socket(self):
        return self.socket

    def open_socket(self):
        try:
            s = socket.socket()
            s.connect((HOST, PORT))
            s.send("PASS " + PASS + "\r\n")
            s.send("NICK " + IDENT + "\r\n")

            with open('joins.txt', 'a+') as jf:
                joins = jf.readlines()

            for chan in joins:
                s.send("JOIN #" + str(chan.strip()) + "\r\n")
                print "joined " + chan.strip()
                sleep(0.50)

            s.send("CAP REQ :twitch.tv/commands\r\n")

            self.socket = s

        except Exception, e:
            print "Opensocket error ", e


socketHelper = SocketHelper()
