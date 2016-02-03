# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
import psutil
import socket

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def main_loop():
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
        from Socket import openSocket, sendMessage, sendChanMsg, joinChan, quitChan, whisperSocket
        from Init import joinRoom
        from Logger import log
        from Api import getUptime, updateMods, restartbot, getSteamStats, convertToSteam64
        from Messagecommands import tryCommands
        
        s = openSocket()
        joinRoom(s)
        s.setblocking(0)
        readbuffer = ""
        elapsed = 0
        end = 0
        reload(sys)
        sys.setdefaultencoding("utf8")
        sendChanMsg(s, "finnishforce_", "started")
        while 1:
                start = timer()
                temp = ""
                user = ""
                
                try:
                        getit = s.recv(4096)
                        readbuffer = readbuffer + getit
                        temp = string.split(readbuffer, "\n")
                        readbuffer = temp.pop()
                except:
                        sleep(0.5)

                if temp != "":
                        for line in temp:
                                try:
                                        
                                        if "PING :tmi.twitch.tv" in line.strip():
                                                s.send("PONG :tmi.twitch.tv\r\n")
                                                break
                                        else:
                                                if "PRIVMSG" in getit:
                                                        user = getUser(line).encode("utf8")
                                                        message = getMessage(line).encode("utf8")
                                                        chan = getChannel(line).encode("utf8")
                                                        time = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
                                                        toLog = user.decode('utf-8') + ": " + message.decode('utf-8')
                                                        log(toLog, chan)
                                                else:
                                                        sleep(0.1)
                                except:
                                        print "error ping"
                
                                       

                if temp != "":
                        if "PRIVMSG" in getit:
                            tryCommands(s, chan, user, message)                                    
                        
                end = timer()
                elapsed = elapsed + (end-start)
                if(elapsed >= 300):
                        s.send("PONG :tmi.twitch.tv\r\n")
                        elapsed = 0




if __name__ == '__main__':
    while 1:
        try:
                print "mainloop"
                main_loop()
        except:
                print "error in mainloop"
                main_loop()

                
