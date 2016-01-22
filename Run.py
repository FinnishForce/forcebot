# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
import psutil

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
        from Socket import openSocket, sendMessage, sendChanMsg, joinChan, quitChan
        from Init import joinRoom
        from Logger import log
        from Api import getUptime, updateMods, restartbot, getSteamStats, convertToSteam64
        from Messagecommands import tryCommands
        
        s = openSocket()
        joinRoom(s)
        s.setblocking(0)
        readbuffer = ""
        num = 0
        elapsed = 0
        end = 0
        dt_uptime = 0
        downtime = 0
        reload(sys)
        sys.setdefaultencoding("utf8")
        #s.send("CAP REQ :twitch.tv/membership")        
        #s.send("CAP REQ :twitch.tv/commands")
        #s.send("CAP REQ :twitch.tv/tags")      
        sendChanMsg(s, "finnishforce_", "started")
        while 1:
                start = timer()
                temp = ""
                user = ""
                
                try:
                        getit = s.recv(4096)
                        #print getit
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

                            #does not work after adding messagecommands.py, need new implementation
                            #if message.startswith("!softresetbot"):
                            #    if user.strip().lower() == "finnishforce_":
                            #        sendChanMsg(s, chan, "DONE!")
                            #        execfile("/home/pi/Desktop/ForceBotti/Run.py")
                        
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

                
