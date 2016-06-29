import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import zipfile
import extract
import downloader
import installer
import re
import time
import common as Common
import wipe
import plugintools
from random import randint
from datetime import date
import calendar
import acdays

addon_id = 'plugin.program.sswizard'
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.sswizard',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
PROFILE  =  os.path.join(USERDATA,'profiles.xml')
LOCK  =  os.path.join(USERDATA,'lock.txt')
NOTICE  =  os.path.join(ADDON,'notice.txt')
WIPE  =  xbmc.translatePath('special://home/wipe.xml')
CLEAN  =  xbmc.translatePath('special://home/clean.xml')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
checkver=my_addon.getSetting('checkupdates')
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR lime]SS[/COLOR] Wizard"
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
SSUpdate = 0
check = plugintools.get_setting("checkupdates")
addonupdate = plugintools.get_setting("updaterepos")

my_date = date.today()
today = calendar.day_name[my_date.weekday()]
OLD = "[COLOR=white]Device Last Cleaned:[/COLOR]"+"\n"
NEW = "[COLOR=white]Device Last Cleaned:[/COLOR] " + str(my_date) + " " + today
automonday = plugintools.get_setting("mondayclean")
CLEANEDTODAY = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedtoday.txt'))

acdays.Checker()

SSOne = "http://pastebin.com/raw/85Ct9Jfi"
SSTwo = "http://pastebin.com/raw/d1DjeFSL"

def Open_URL(url):
        req      = urllib2.Request(url)
        req.add_header('User-Agent','TheWizardIsHere')
        response = urllib2.urlopen(req)
        link     = response.read()
        response.close()

        return link.replace('\r','').replace('\n','').replace('\t','')

nointernet = 0

try:
        response = Open_URL(GoogleOne)
except:
        try:
                response = Open_URL(GoogleTwo)
        except:
                dialog.ok(AddonTitle,'Sorry we are unable to check for updates!','The device is not connected to the internet','Please check your connection settings.')
                nointernet = 1
                pass

try:
        response = Open_URL(SSTwo)
except:
        SSUpdate = 1

if nointernet == 0 and SSUpdate == 0:
        if check == 'true':
                if os.path.exists(CHECKVERSION):
                        checkurl = SSTwo
                        vers = open(CHECKVERSION, "r")
                        regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
                        for line in vers:
                                currversion = regex.findall(line)
                                for build,vernumber in currversion:
                                        if vernumber > 0:
                                                req = urllib2.Request(checkurl)
                                                req.add_header('User-Agent','TheWizardIsHere')
                                                try:
                                                        response = urllib2.urlopen(req)
                                                except:
                                                        dialog.ok(AddonTitle,'Sorry we are unable to check for [B]JARVIS[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')							   
                                                        sys.exit(1)

                                                link=response.read()
                                                response.close()
                                                match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
                                                for newversion,fresh in match:
                                                        if newversion > vernumber:
                                                                if fresh =='false': # TRUE
                                                                        choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                                                                        if choice == 1: 
                                                                                updateurl = SSOne
                                                                                req = urllib2.Request(updateurl)
                                                                                req.add_header('User-Agent','TheWizardIsHere')
                                                                                try:
                                                                                        response = urllib2.urlopen(req)
                                                                                except:
                                                                                        dialog.ok(AddonTitle,'Sorry we were unable to download the update!','The update host appears to be down.','Please check for updates later via the wizard.')
                                                                                        sys.exit(1)
                                                                                link=response.read()
                                                                                response.close()
                                                                                match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
                                                                                for url in match:				
                                                                                        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                                                                                        name = "build"
                                                                                        dp = xbmcgui.DialogProgress()

                                                                                        dp.create(AddonTitle,"Downloading ",'', 'Please Wait')
                                                                                        lib=os.path.join(path, name+'.zip')
                                                                                        try:
                                                                                                os.remove(lib)
                                                                                        except:
                                                                                                pass

                                                                                        downloader.download(url, lib, dp)
                                                                                        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
                                                                                        time.sleep(2)
                                                                                        dp.update(0,"", "Extracting Zip Please Wait")
                                                                                        installer.unzip(lib,addonfolder,dp)
                                                                                        dialog = xbmcgui.Dialog()
                                                                                        dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")							
                                                                                        Common.killxbmc()
                                                                        else:
                                                                                sys.exit(1)
                                                                else:
                                                                        choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                                                                        if choice == 1: 
                                                                                dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[COLOR snow]If you wish to update later you can do so in [/COLOR][COLOR lime]SS[/COLOR] Wizard')
                                                                                wipe.FRESHSTART()
                                                                        else:
                                                                                sys.exit(1)

if addonupdate == 'true':
        #Update all repos and packages.
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")