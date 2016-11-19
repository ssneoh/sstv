import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import platform
import urllib2,urllib
from urllib import FancyURLopener
import re
import speedtest
import glob
import common as Common
import wipe
import installer
import update
import parameters
import maintenance
import plugintools
import backuprestore
import base64
import socket
import json
import runner
import shutil
import requests

AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.sswizard'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
BASEURL = "http://ssneoh.site88.net/"
SpeedTest = "http://pastebin.com/raw/gL8qCbEJ"
wizard_rel = "http://pastebin.com/raw/Q60AX7Rz"

DEFAULT_SETTINGS    =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'resources/settings_default.xml'))
ADDON_DATA          =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
USER_SETTINGS       =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'settings.xml'))


params=parameters.get_params()
runner.check()

#######################################################################
#			CREATE USER SETTINGS XML IF IT DOES NOT EXIST
#######################################################################

if not os.path.isfile(USER_SETTINGS):
        if not os.path.exists(ADDON_DATA):
                os.makedirs(ADDON_DATA)
        shutil.copyfile(DEFAULT_SETTINGS, USER_SETTINGS)

#######################################################################
#						ROOT MENU
#######################################################################

def INDEX():
        Common.addDir('Install Builds',BASEURL,10,ART+'install.png',FANART,'')
        Common.addDir('Backup | Restore',BASEURL,30,ART+'backuprestore.png',FANART,'')
        Common.addDir('Maintenance',BASEURL,20,ART+'clean.png',FANART,'')
        Common.addDir('Tools',BASEURL,40,ART+'tool.png',FANART,'')


def BUILDMENU():

        link = Common.OPEN_URL(wizard_rel).replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
                Common.addDir(name + " [COLOR gold]Ver:[/COLOR] [COLOR lime]" + description + "[/COLOR]",url,11,iconimage,fanart,description)

#######################################################################
#						MAINTENANCE MENU
#######################################################################

def get_size(start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
        return total_size

def convertSize(size):
        import math
        if (size == 0):
                return '[COLOR lime][B]0 MB[/COLOR][/B]'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        if size_name[i] == "B":
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if size_name[i] == "KB":
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if size_name[i] == "GB":
                return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if size_name[i] == "TB":
                return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s < 50:
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s >= 50:
                if s < 100:
                        return '[COLOR orange][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s >= 100:
                return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'

def convertSizeInstall(size):
        import math
        if (size == 0):
                return '[COLOR lime][B]0 MB[/COLOR][/B]'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        if size_name[i] == "B":
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if size_name[i] == "KB":
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if size_name[i] == "TB":
                return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s < 1000:
                return '[COLOR lime][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s >= 1000:
                if s < 1500:
                        return '[COLOR orange][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
        if s >= 1500:
                return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'

def maintMenu():

        HOME          =  xbmc.translatePath('special://home/')
        PACKAGES      =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
        THUMBS        =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))
        CACHE_FOLDER  =  xbmc.translatePath(os.path.join('special://home','cache'))
        TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://','temp'))
        CACHE         =  "NULL"

        if os.path.exists(CACHE_FOLDER):
                CACHE = CACHE_FOLDER

        if os.path.exists(TEMP_FOLDER):
                CACHE = TEMP_FOLDER

        if not os.path.exists(PACKAGES):
                os.makedirs(PACKAGES)

        if CACHE == "NULL":
                try:
                        PACKAGES_SIZE_BYTE = get_size(PACKAGES)
                        THUMB_SIZE_BYTE    = get_size(THUMBS)
                except: pass
        else:
                try:
                        CACHE_SIZE_BYTE    = get_size(CACHE)
                        PACKAGES_SIZE_BYTE = get_size(PACKAGES)
                        THUMB_SIZE_BYTE    = get_size(THUMBS)
                except: pass

        if CACHE == "NULL":
                try:
                        PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
                        THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)
                except: pass
        else:
                try:
                        CACHE_SIZE    = convertSize(CACHE_SIZE_BYTE)
                        PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
                        THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)
                except: pass

        if CACHE == "NULL":
                CACHE_SIZE    =  "[COLOR red][B]ERROR READING CACHE[/B][/COLOR]"

        startup_clean = plugintools.get_setting("acstartup")
        weekly_clean = plugintools.get_setting("clearday")
        sizecheck_clean = plugintools.get_setting("startupsize")

        if startup_clean == "false":
                startup_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
        else:
                startup_onoff = "[COLOR lime][B]ON[/COLOR][/B]"
        if weekly_clean == "0":
                weekly_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
        else:
                weekly_onoff = "[COLOR lime][B]ON[/COLOR][/B]"
        if sizecheck_clean == "false":
                sizecheck_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
        else:
                sizecheck_onoff = "[COLOR lime][B]ON[/COLOR][/B]"


        Common.addItem('[COLOR dodgerblue]Auto Clean On Startup - [/COLOR]' + startup_onoff,BASEURL,110,ART+'system.png',FANART,'')
        Common.addItem('[COLOR dodgerblue]Weekly Auto Clean - [/COLOR]' + weekly_onoff,BASEURL,111,ART+'system.png',FANART,'')
        Common.addItem('[COLOR dodgerblue]Auto Clear At Specific MB - [/COLOR]' + sizecheck_onoff,BASEURL,29,ART+'system.png',FANART,'')
        Common.addItem("[COLOR powderblue][B]--------------------------[/B][/COLOR]",BASEURL,'',ICON,FANART,'')
        Common.addItem("[COLOR white]CACHE SIZE: [/COLOR]" + str(CACHE_SIZE),BASEURL,'',ICON,FANART,'')
        Common.addItem("[COLOR white]PACKAGES SIZE: [/COLOR]" + str(PACKAGES_SIZE),BASEURL,'',ICON,FANART,'')
        Common.addItem("[COLOR white]THUMBNAIL SIZE: [/COLOR]" + str(THUMB_SIZE),BASEURL,'',ICON,FANART,'')
        Common.addItem("[COLOR powderblue][B]--------------------------[/B][/COLOR]",BASEURL,'',ICON,FANART,'')        
        Common.addDir('[COLOR white]Auto Clean Device[/COLOR]','url',21,ART+'clean.png',FANART,'')
        Common.addItem('[COLOR white]Clear Cache[/COLOR]','url',22,ART+'clean.png',FANART,'')
        Common.addItem('[COLOR white]Delete Thumbnails[/COLOR]','url',23,ART+'clean.png',FANART,'')
        Common.addItem('[COLOR white]Purge Packages[/COLOR]','url',24,ART+'clean.png',FANART,'')


def tools():

        cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
        tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
        WindowsCache = xbmc.translatePath('special://home')
        i = 0

        if os.path.exists(tempPath):
                for root, dirs, files in os.walk(tempPath,topdown=True):
                        dirs[:] = [d for d in dirs]
                        for name in files:
                                if ".old.log" not in name.lower():
                                        if ".log" in name.lower():
                                                a=open((os.path.join(root, name))).read()       
                                                b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                                                match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                                                for checker in match:
                                                        i = i + 1

        if os.path.exists(WindowsCache):
                for root, dirs, files in os.walk(WindowsCache,topdown=True):
                        dirs[:] = [d for d in dirs]
                        for name in files:
                                if ".old.log" not in name.lower():
                                        if ".log" in name.lower():
                                                a=open((os.path.join(root, name))).read()       
                                                b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                                                match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                                                for checker in match:
                                                        i = i + 1

        if i == 0:
                ERRORS_IN_LOG = "[COLOR lime][B]0 ERRORS FOUND IN LOG[/B][/COLOR]"
        else:
                ERRORS_IN_LOG = "[COLOR red][B]" + str(i) + " ERRORS FOUND IN LOG[/B][/COLOR]"


        Common.addItem('Convert Physical Paths To Special','url',41,ART+'convert.png',FANART,'')
        Common.addItem('Check For Updates',BASEURL,42,ART+'update.png',FANART,'')
        Common.addItem('View Current or Old Log File','url',46,ART+'log.png',FANART,'')
        Common.addItem('View The Last Error In Log File','url',48,ART+'log.png',FANART,'')
        Common.addItem('View All ' + str(i) + ' Errors In Log File','url',49,ART+'log.png',FANART,'')
        Common.addItem('Delete Crash Logs','url',47,ART+'log.png',FANART,'')
        Common.addItem('Check for Broken Repositories','url',50,ART+'tool.png',FANART,'')
        Common.addItem('Check for Broken Sources in sources.xml','url',51,ART+'tool.png',FANART,'')
        Common.addDir('Speed Test',BASEURL,43,ART+'speed.png',FANART,'')
        Common.addDir('System Reset [COLOR red](CAUTION)[/COLOR]','url',44,ART+'systemreset.png',FANART,'')


#######################################################################
#						SPEEDTEST LIST
#######################################################################

def SPEEDTEST():

        link = Common.OPEN_URL(SpeedTest).replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
                Common.addItem('[COLOR ghostwhite]' + name + " | " + description + '[/COLOR]',url,45,ART+'speed.png',FANART,'')

#######################################################################
#						BACKUP MENU MENU
#######################################################################

def BACKUPMENU():

        Common.addItem('Backup','url',31,ART+'backuprestore.png',FANART,'')
        Common.addDir('Restore','url',32,ART+'backuprestore.png',FANART,'')
        Common.addDir('Delete A Backup','url',33,ART+'backuprestore.png',FANART,'')
        Common.addItem('Delete All Backups','url',34,ART+'backuprestore.png',FANART,'')
        Common.addItem('Select Backup Location','url',29,ART+'backuprestore.png',FANART,'')

#######################################################################
#                       Compatibility
#######################################################################
############################
###SET VIEW#################
############################

def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view')=='true':
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

##############################    END    #########################################

#######################################################################
#					OPEN THE SETTINGS DIALOG
#######################################################################

def OPEN_SETTINGS(params):
        plugintools.open_settings_dialog()
        xbmc.executebuiltin("Container.Refresh")

#######################################################################
#						Which mode to select
#######################################################################

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==10:
        BUILDMENU()

elif mode==11:
        installer.INSTALL(name,url,description)

elif mode==20:
        maintMenu()

elif mode==21:
        maintenance.autocleanask()

elif mode==22:
        maintenance.clearCache()

elif mode==23:
        maintenance.deleteThumbnails()

elif mode==24:
        maintenance.purgePackages()

elif mode==29:
        OPEN_SETTINGS(params)

elif mode==30:
        BACKUPMENU()

elif mode==31:
        backuprestore.Backup()

elif mode==32:
        backuprestore.Restore()

elif mode==33:
        backuprestore.ListBackDel()

elif mode==34:
        backuprestore.DeleteAllBackups()

elif mode==40:
        tools()

elif mode==41:
        maintenance.Fix_Special(url)

elif mode==42:
        update.updateaddons()

elif mode==43:
        SPEEDTEST()

elif mode==44:
        wipe.FRESHSTART()

elif mode==45:
        speedtest.runtest(url)

elif mode==46:
        maintenance.viewLogFile()

elif mode==47:
        maintenance.DeleteCrashLogs()

elif mode==48:
        maintenance.view_LastError()

elif mode==49:
        maintenance.viewErrors()

elif mode==50:
        maintenance.CHECK_BROKEN_REPOS()

elif mode==51:
        maintenance.CHECK_BROKEN_SOURCES()

elif mode==100:
        backuprestore.READ_ZIP(url)

elif mode==101:
        backuprestore.DeleteBackup(url)

elif mode==102:
        xbmc.executebuiltin(description)
        sys.exit(0)

elif mode==103:
        backuprestore.BACKUP_RD_TRAKT()

elif mode==104:
        backuprestore.RESTORE_RD_TRAKT()

elif mode==105:
        backuprestore.READ_ZIP_TRAKT(url)

elif mode==107:
        backuprestore.TV_GUIDE_BACKUP()

elif mode==108:
        backuprestore.ADDON_DATA_BACKUP()

elif mode==109:
        maintenance.RUYA_FIX()

elif mode==110:
        maintenance.AUTO_CLEAN_ON_OFF()

elif mode==111:
        maintenance.AUTO_WEEKLY_CLEAN_ON_OFF()

xbmcplugin.endOfDirectory(int(sys.argv[1]))