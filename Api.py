import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import websocket
from datetime import datetime, timedelta, date, time
from time import sleep
steamapikey = "xyz"

def getSteamStats(steamid):
        try:
                favs = ['1','Desert Eagle','2','Dual Berettas','3','Five-SeveN','4','Glock-18','7','AK-47','8','AUG','9','AWP','10','FAMAS','11','G3SG1','13','Galil AR','14','M249','16','M4A4 or A1','17','MAC-10','19','P90','35','Nova','60','M4A1-S','24','UMP-45','25','XM1014','26','PP-Bizon','27','MAG-7','28','Negev','29','Sawed-Off','30','Tec-9','31','Zeus x27','32','P2000','33','MP7','34','MP9','36','P250','38','SCAR-20','39','SG 553','40','SSG 08','42','Knife','61','USP-S','63','CZ75-Auto']
                favweapon = "null"
                totalwins = 0
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == 'last_match_t_wins':
                                t_wins = entry['value']
                        if entry['name'] == 'last_match_ct_wins':
                                ct_wins = entry['value']
                                totalwins = t_wins + ct_wins
                        if entry['name'] == 'last_match_wins':
                                last_wins = entry['value']
                                last_loses = totalwins-last_wins
                        if entry['name'] == 'last_match_kills':
                                last_kills = entry['value']
                        if entry['name'] == 'last_match_deaths':
                                last_deaths = entry['value']
                        if entry['name'] == 'last_match_mvps':
                                last_mvps = entry['value']
                        if entry['name'] == 'last_match_favweapon_id':
                                favweapon_id = entry['value']
                                for i, j in zip(favs, favs[1:]):
                                        if str(favweapon_id) == str(i):
                                                favweapon = j
                                                break
                                
                        if entry['name'] == 'last_match_favweapon_shots':
                                favweapon_shots = entry['value']
                        if entry['name'] == 'last_match_favweapon_hits':
                                favweapon_hits = entry['value']
                        if entry['name'] == 'last_match_favweapon_kills':
                                favweapon_kills = entry['value']
                        if entry['name'] == 'last_match_damage':
                                last_damage = entry['value']
                        if entry['name'] == 'last_match_money_spent':
                                last_money_spent = entry['value']
                if last_deaths > 0:
                        kd = last_kills/float(last_deaths)
                else:
                        kd = last_kills
                kd = round(kd, 2)
                if favweapon_shots > 0:
                        accuracy = favweapon_hits/float(favweapon_shots)
                else:
                        accuracy = 0
                accuracy = accuracy * 100
                accuracy = round(accuracy, 1)
                
                if (last_wins > last_loses):
                        result = "Won"
                elif (last_wins == last_loses):
                        result = "Tied"
                else:
                        result = "Lost"
                        
                if (totalwins < 16):
                        result = "Score:"
                playerName = ""
                playerName = getPlayerName(steamid)
                
                roundscore = playerName + "'s last game: " + result + " " + str(last_wins) + "-" + str(last_loses)
                koodee = str(last_kills) + "K/" + str(last_deaths) + "D (" + str(kd) + " KD), " + str(last_mvps) + " MVPS"
                favwpn = "Favourite weapon: " + str(favweapon) + " with " + str(favweapon_kills) + " kills (" + str(favweapon_shots) + " shots, " + str(favweapon_hits) + " hits, " + str(accuracy) + "% accuracy)"
                uselessinfo = "Damage dealt: " + str(last_damage) + ", money spent: " + str(last_money_spent)
                resp = roundscore + " -- " + koodee + " -- " + favwpn + " -- " + uselessinfo
                return resp
                                
                
        except:
                print "getSteamStats api.py error"

def getUptime(chan):

        try:    
                url = ("https://api.twitch.tv/kraken/streams/" + chan)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)

                if page['stream'] == None:
                        return "0:00:00 (stream offline)"

                started = page['stream']['created_at']
                timeFormat = "%Y-%m-%dT%H:%M:%SZ"
                startdate = datetime.strptime(started, timeFormat)
                current = datetime.utcnow()
                combined = current - startdate - timedelta(microseconds=current.microsecond)
                return str(combined)

        except:
                print "getuptime api.py error" + datetime.utcnow()

def updateMods(chan):
        try:    
                url = ("http://tmi.twitch.tv/group/user/" + chan + "/chatters")
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                
                if page['chatters']['moderators'] == None:
                        print "no moderators"
                        return 0                
                
                apimods = page['chatters']['moderators']
                addc = 0
                chanmods = chan + 'mods.txt'
                modsfile = open(chanmods, 'a+')
                mods = modsfile.readlines()
                if not mods:
                        modsfile.write(chan.encode('utf8') + '\n'.encode('utf8'))

                for somethings in mods:
                        if mods[addc].strip().decode('utf8') == apimods[addc].decode('utf8'):
                                sleep(0.1)
                        else:
                                modsfile.write(apimods[addc].encode('utf8') + '\n'.encode('utf8'))
                        
                        addc = addc + 1


                modsfile.close()

        except:
                print "updatemods api.py error"

def restartbot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def convertToSteam64(vanity):
        
        try:
                url = ("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steamapikey + "&vanityurl=" + vanity)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                if page['response']['success'] == 1:
                        steam64id = page['response']['steamid']
                        return steam64id
                else:
                        print "vanity url not found"
        except:
                print "error in convertToSteam64"

def getTussariKills(steamid):
        try:
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == 'total_kills_nova':
                                novakills = entry['value']
                playerName = getPlayerName(steamid)
                resp = playerName + " has " + str(novakills) + " kills with tussari"
                return resp
        except:
                print "tussarikills error"

def getPlayerName(steamid):
        try:
                playerName = "null"
                url = ("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamapikey + "&steamids=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['response']['players']:
                        playerName = entry['personaname']
                return playerName
                
        except:
                print "error in getPlayerName"


def getPlayerBans(steamid):
        try:
                playerName = "null"
                url = ("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=" + steamapikey + "&steamids=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['players']:
                        vacs = entry['NumberOfVACBans']
                        lastban = entry['DaysSinceLastBan']
                        gamebans = entry['NumberOfGameBans']
                        ecoban = entry['EconomyBan']
                        
                playerName = getPlayerName(steamid)
                
                if lastban == 0 and vacs == 0 and gamebans == 0:
                        lastban = ""
                else:
                        lastban = str(lastban) + " days since last VAC/game ban."
                        
                resp = "User " + playerName + " has " + str(vacs) + " VAC bans and " + str(gamebans) +" game bans. " + "Trade ban status: "  + str(ecoban) + ". " + str(lastban)
                return resp
        except:
                print "error in getPlayerBans"
                        

def getKills(steamid, wpn):
        try:
                what = 'total_kills_' + wpn.strip()
                what = what.lower()
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == what:
                                kills = entry['value']
                playerName = getPlayerName(steamid)
                resp = playerName + " has " + str(kills) + " kills with " + wpn
                return resp
        except:
                print "getkills error"


def getJoin():
        try:
                html_page = urllib2.urlopen("http://steamcommunity.com/profiles/76561198185015081/")
                soup = BeautifulSoup(html_page, "html.parser")
                for link in soup.findAll('a', attrs={'href': re.compile("^steam://")}):
                        if link.get('href') == "steam://":
                                return "Joining not possible at the moment."
                        else:
                                return link.get('href')
        except:
                return "Joining not possible at the moment."


def getViewers(chan):
        try:
                url = ("https://tmi.twitch.tv/group/user/" + chan + "/chatters")
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                viewers = []
                for entry in page['chatters']['moderators']:
                        viewers.append(entry)
                for entry in page['chatters']['staff']:
                        viewers.append(entry)
                for entry in page['chatters']['admins']:
                        viewers.append(entry)
                for entry in page['chatters']['global_mods']:
                        viewers.append(entry)
                for entry in page['chatters']['viewers']:
                        viewers.append(entry)
                        
                return viewers

                
        except:
                print "getviewers error"


def getViewerAmount(chan):
        try:
                url = ("https://tmi.twitch.tv/group/user/" + chan + "/chatters")
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                amount = page['chatter_count']

                return amount
        except:
                print "getvieweramount error"

                
