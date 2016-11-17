import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import shutil
import zipfile
import extract
import downloader
import maintenance
import installer
import re
import backuprestore
import time
import common as Common
import wipe
import runner
import plugintools
from random import randint
from datetime import date
import calendar
import acdays

my_date = date.today()
today = calendar.day_name[my_date.weekday()]
addon_id = 'plugin.program.sswizard'
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.sswizard',''))
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
check = plugintools.get_setting("checkupdates")
addonupdate = plugintools.get_setting("updaterepos")
size_check = plugintools.get_setting("startupsize")
autoclean = plugintools.get_setting("acstartup")
CLEAR_CACHE_SIZE = plugintools.get_setting("cachemb")
CLEAR_PACKAGES_SIZE = plugintools.get_setting("packagesmb")
CLEAR_THUMBS_SIZE = plugintools.get_setting("thumbsmb")
BASEURL = 'http://ssneoh.site88.net'
update_wiz = 'http://pastebin.com/raw/85Ct9Jfi'
version_check = 'http://pastebin.com/raw/d1DjeFSL'
nointernet = 0

#Update Information
SS_VERSION  =  os.path.join(USERDATA,'version.txt')
HOME         =  xbmc.translatePath('special://home/')
TMP_TRAKT     =  xbmc.translatePath(os.path.join(HOME,'tmp_trakt'))
TRAKT_MARKER =  xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))

if os.path.isfile(TRAKT_MARKER):
        choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR lime][B]A backup of your Real Debrid & Trakt settings has been found.[/B][COLOR]','[COLOR red][B]SELECTING NO WILL LOSE ALL SETTINGS[/COLOR][/B]','[COLOR yellow]Do you want to resotre those settings now?[/COLOR]',nolabel='[B][COLOR red]NO[/COLOR][/B]',yeslabel='[B][COLOR lime]YES[/COLOR][/B]')
        if choice == 1:
                backuprestore.AUTO_READ_ZIP_TRAKT(backup_zip)
        else:
                choice2 = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]YOU HAVE CHOSEN NOT TO RESTORE YOUR SETTINGS.[/B][/COLOR]','[COLOR red][B]YOU WILL NOT HAVE THIS OPTION AGAIN[/COLOR][/B]','[COLOR red][B]ARE YOU SURE YOU WANT TO COMPLETE THIS ACTION?[/B][/COLOR]',yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                if choice2 == 0:
                        backuprestore.AUTO_READ_ZIP_TRAKT(backup_zip)
                else:
                        _out = xbmc.translatePath(os.path.join('special://','home/tmp_trakt'))
                        try:
                                shutil.rmtree(_out)
                                shutil.rmdir(_out)
                        except: pass

runner.check()

#Check Internet Connection
try:
        response = Common.OPEN_URL_NORMAL(GoogleOne)
except:
        try:
                response = Common.OPEN_URL_NORMAL(GoogleTwo)
        except:
                dialog.ok(AddonTitle,'Sorry we are unable to check for updates!','The device is not connected to the internet','Please check your connection settings.')
                nointernet = 1
                pass

#######################################################################
#						Check for Updates
#######################################################################

pleasecheck = 0

#Information for SS Wizard OTA updates.
if os.path.exists(SS_VERSION):
        VERSIONCHECK = SS_VERSION
        FIND_URL = update_wiz
        checkurl = version_check
        pleasecheck = 1

if nointernet == 0 and pleasecheck == 1:
        if check == 'true':
                if os.path.exists(VERSIONCHECK):
                        vers = open(VERSIONCHECK, "r")
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
                                                        dialog.ok(AddonTitle,'Sorry we are unable to check for updates!','The update host appears to be down.','Please check for updates later via the wizard.')							   
                                                        sys.exit(1)

                                                link=response.read()
                                                response.close()
                                                match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
                                                for newversion,fresh in match:
                                                        if newversion > vernumber:
                                                                if fresh =='false': # TRUE
                                                                        choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                                                                        if choice == 1: 
                                                                                updateurl = FIND_URL
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
                                                                                dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[COLOR snow]If you wish to update later you can do so in [/COLOR][COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]')
                                                                                wipe.FRESHSTART()
                                                                        else:
                                                                                sys.exit(1)

if addonupdate == 'true':
        #Update all repos and packages.
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")

        if autoclean == "true":
                maintenance.Auto_Startup()
        
        CACHE      =  xbmc.translatePath(os.path.join('special://home/cache',''))
        PACKAGES   =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
        THUMBS     =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))
        
        if not os.path.exists(CACHE):
                CACHE     =  xbmc.translatePath(os.path.join('special://home/temp',''))
        if not os.path.exists(PACKAGES):
                os.makedirs(PACKAGES)
        
        if not CLEAR_CACHE_SIZE == "0":
                if CLEAR_CACHE_SIZE == "1":
                        CACHE_TO_CLEAR = 25000000
                if CLEAR_CACHE_SIZE == "2":
                        CACHE_TO_CLEAR = 50000000
                if CLEAR_CACHE_SIZE == "3":
                        CACHE_TO_CLEAR = 75000000
                if CLEAR_CACHE_SIZE == "4":
                        CACHE_TO_CLEAR = 100000000
        
                CACHE_SIZE_BYTE    = Common.get_size(CACHE)
        
                if  CACHE_SIZE_BYTE > CACHE_TO_CLEAR:
                        maintenance.AUTO_CLEAR_CACHE_MB()
        
        if not CLEAR_PACKAGES_SIZE == "0":
                if CLEAR_PACKAGES_SIZE == "1":
                        PACKAGES_TO_CLEAR = 25000000
                if CLEAR_PACKAGES_SIZE == "2":
                        PACKAGES_TO_CLEAR = 50000000
                if CLEAR_PACKAGES_SIZE == "3":
                        PACKAGES_TO_CLEAR = 75000000
                if CLEAR_PACKAGES_SIZE == "4":
                        PACKAGES_TO_CLEAR = 100000000
        
                PACKAGES_SIZE_BYTE    = Common.get_size(PACKAGES)
        
                if PACKAGES_SIZE_BYTE > PACKAGES_TO_CLEAR:
                        if not xbmc.getCondVisibility("Window.isVisible(ProgressDialog)"):
                                maintenance.AUTO_CLEAR_PACKAGES_MB()
        
        if not CLEAR_THUMBS_SIZE == "0":
                if CLEAR_THUMBS_SIZE == "1":
                        THUMBS_TO_CLEAR = 25000000
                if CLEAR_THUMBS_SIZE == "2":
                        THUMBS_TO_CLEAR = 50000000
                if CLEAR_THUMBS_SIZE == "3":
                        THUMBS_TO_CLEAR = 75000000
                if CLEAR_THUMBS_SIZE == "4":
                        THUMBS_TO_CLEAR = 100000000
        
                THUMBS_SIZE_BYTE    = Common.get_size(THUMBS)
        
                if  THUMBS_SIZE_BYTE > THUMBS_TO_CLEAR:
                        maintenance.AUTO_CLEAR_THUMBS_MB()
        
        if size_check == "true":
        
                CACHE_SIZE_BYTE    = Common.get_size(CACHE)
                PACKAGES_SIZE_BYTE    = Common.get_size(PACKAGES)
                THUMBS_SIZE_BYTE    = Common.get_size(THUMBS)
        
                if CACHE_SIZE_BYTE >= 100000000:
                        choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Cache is now over 100 MB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO CLEAR THE CACHE NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
                        if choice == 1: 
                                xbmc.executebuiltin( "ActivateWindow(busydialog)" )
                                maintenance.AUTO_CLEAR_CACHE_MB()
                                xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                dialog = xbmcgui.Dialog()
                                dialog.ok(AddonTitle, "Your cache has been successfully cleared.","")							
        
                if PACKAGES_SIZE_BYTE >= 1000000000:
                        if not xbmc.getCondVisibility("Window.isVisible(ProgressDialog)"):
                                choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Packages folder is now over 1 GB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO PURGE THE PACKAGES NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
                                if choice == 1:
                                        xbmc.executebuiltin( "ActivateWindow(busydialog)" )
                                        maintenance.AUTO_CLEAR_PACKAGES_MB()
                                        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                        dialog = xbmcgui.Dialog()
                                        dialog.ok(AddonTitle, "Your packages have been successfully purged.","")							
        
                if THUMBS_SIZE_BYTE >= 300000000:
                        choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Thumbnails are now over 300 MB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO CLEAR THE THUMBNAILS NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
                        if choice == 1: 
                                xbmc.executebuiltin( "ActivateWindow(busydialog)" )
                                maintenance.AUTO_CLEAR_THUMBS_MB()
                                xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                dialog = xbmcgui.Dialog()
                                dialog.ok(AddonTitle, "Your thumbnails have been successfully cleared.","")							
        
        #Call the daily auto cleaner script.
        acdays.Checker()