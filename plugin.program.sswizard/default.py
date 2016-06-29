import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import platform
import urllib2,urllib
import re
import speedtest
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

AddonTitle="[COLOR lime]SS[/COLOR] Wizard"
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.sswizard'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
BASEURL = "http://www.sstv.com"
SpeedTest = "http://pastebin.com/raw/gL8qCbEJ"

params=parameters.get_params()

#######################################################################
#						ROOT MENU
#######################################################################

def INDEX():
        Common.addDir('Install Builds',BASEURL,10,ART+'install.png',FANART,'')
        Common.addDir('Backup | Restore',BASEURL,30,ART+'backuprestore.png',FANART,'')
        Common.addDir('Maintenance',BASEURL,20,ART+'clean.png',FANART,'')
        Common.addDir('Tools',BASEURL,40,ART+'tool.png',FANART,'')


def BUILDMENU():

        link = Common.OPEN_URL('http://pastebin.com/raw/Q60AX7Rz').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
                Common.addDir(name + " [COLOR gold]Ver:[/COLOR] [COLOR magenta]" + description + "[/COLOR]",url,11,iconimage,fanart,description)


def maintMenu():

        Common.addDir('Auto Clean Device','url',21,ART+'clean.png',FANART,'')
        Common.addItem('Clear Cache','url',22,ART+'clean.png',FANART,'')
        Common.addItem('Delete Thumbnails','url',23,ART+'clean.png',FANART,'')
        Common.addItem('Purge Packages','url',24,ART+'clean.png',FANART,'')


def tools():

        Common.addItem('Convert Physical Paths To Special','url',41,ART+'convert.png',FANART,'')
        Common.addItem('Check For Updates',BASEURL,42,ART+'update.png',FANART,'')
        Common.addItem('View Current or Old Log File','url',46,ART+'log.png',FANART,'')
        Common.addItem('Delete Crash Logs','url',47,ART+'log.png',FANART,'')
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

xbmcplugin.endOfDirectory(int(sys.argv[1]))