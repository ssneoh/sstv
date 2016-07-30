import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import re
import urllib,urllib2
import time
import common as Common
import shutil
import skinSwitch

thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.sswizard')
mediaPath = os.path.join(addonPath, 'resources/art')
databasePath = xbmc.translatePath('special://userdata/Database')
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.sswizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.sswizard'
AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
MaintTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
dialog       =  xbmcgui.Dialog()
HOME         =  xbmc.translatePath('special://home/')
dp           =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
USB          =  xbmc.translatePath(os.path.join(HOME,'backupdir'))
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.19"
DBPATH = xbmc.translatePath('special://userdata/Database')
TNPATH = xbmc.translatePath('special://userdata/Thumbnails');
PATH = "SS Wizard"            
BASEURL = "http://ssneoh.site88.net/"
H = 'http://'
skin         =  xbmc.getSkinDir()
EXCLUDES     = ['tmp_trakt','EXCLUDES','Database','backupdir','plugin.program.sswizard','script.module.requests','repository.ssneoh.kodi']
EXCLUDES_FILES     = ""
ARTPATH      =  '' + os.sep
UPDATEPATH     =  xbmc.translatePath(os.path.join('special://home/addons',''))
UPDATEADPATH	=  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
EXCLUDES_FOLDER     =  xbmc.translatePath(os.path.join(USERDATA,'EXCLUDES'))
ADDON_DATA     =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
WIPE 		 =  xbmc.translatePath('special://home/wipe.xml')
MARKER          =  xbmc.translatePath(os.path.join(USERDATA,'MARKER.txt'))
CLEAN 		 =  xbmc.translatePath('special://home/clean.xml')
FRESH        = 0
BASEURL = 'http://ssneoh.site88.net/'
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
SKINPATH  =  xbmc.translatePath(os.path.join(ADDONS,skin))
NAVI  =  xbmc.translatePath(os.path.join(ADDONS,'script.navi-x'))
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
zip = 'special://home/addons/plugin.program.sswizard'
urlbase      =  'None'
mastercopy   =  ADDON.getSetting('mastercopy')
dialog = xbmcgui.Dialog()
urlupdate =  ""
updatename =  "ss_update"
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
checkver=my_addon.getSetting('checkupdates')
dialog = xbmcgui.Dialog()

#Real Debrid and Trakt Files
Trakt_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'script.trakt'))
URL_Resolver_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'script.module.urlresolver'))
Exodus_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.exodus'))
Salts_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.salts'))
SaltsLite_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.saltshd.lite'))
Velocity_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.velocity'))
VelocityKids_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.velocitykids'))
TheRoyalWe_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.theroyalwe'))
Specto_AD     =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.specto'))

def FRESHSTART():

        choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]ARE YOU SURE YOU WANT TO RESTORE THE SYSTEM?[/B][/COLOR]',' ' ,'[COLOR orange]Everything EXCEPT this WIZARD will be REMOVED.[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
        if choice == 0:
                sys.exit(1)

        skin         =  xbmc.getSkinDir()
        KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
        skinswapped = 0

        #SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
        if skin not in ['skin.confluence','skin.estuary']:
                choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]YOU ARE NOT USING THE DEFAULT SKIN.[/B][/COLOR]','[COLOR orange]Click YES to attempt to AUTO SWITCH the skin[/COLOR]','[COLOR red]Please DO NOT PRESS ANY BUTTONS or MOVE THE MOUSE while the process is taking place, it is AUTOMATIC[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                if choice == 0:
                        sys.exit(1)
                skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
                skinSwitch.swapSkins(skin)
                skinswapped = 1
                time.sleep(1)

        #IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
        if skinswapped == 1:
                if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                        xbmc.executebuiltin( "Action(Select)" )

        #IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
        if skinswapped == 1:
                while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                        time.sleep(1)

        #WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
        if skinswapped == 1:
                while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                        xbmc.executebuiltin( "Action(Left)" )
                        xbmc.executebuiltin( "Action(Select)" )
                        time.sleep(1)

        skin         =  xbmc.getSkinDir()

        #CHECK IF THE SKIN IS NOT CONFLUENCE
        if skin not in ['skin.confluence','skin.estuary']:
                choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR red]Click YES to MANUALLY SWITCH the skin now[/COLOR]','[COLOR red]You can press NO and attempt the AUTO SWITCH again if you wish[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                if choice == 1:
                        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
                        return
                else:
                        sys.exit(1)

        dp.create(AddonTitle,"Restoring Kodi.",'In Progress...', 'Please Wait')
        try:
                for root, dirs, files in os.walk(HOME,topdown=True):
                        dirs[:] = [d for d in dirs if d not in EXCLUDES]
                        for name in files:
                                try:
                                        os.remove(os.path.join(root,name))
                                        os.rmdir(os.path.join(root,name))
                                except: pass

                        for name in dirs:
                                try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                except: pass
        except: pass

        dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()

        if os.path.exists(NAVI):
                try:
                        shutil.rmtree(NAVI)
                except:
                        pass

        if os.path.exists(DATABASE):
                try:
                        for root, dirs, files in os.walk(DATABASE,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

        if os.path.exists(ADDON_DATA):
                try:
                        for root, dirs, files in os.walk(ADDON_DATA,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

        Common.killxbmc()

def WIPERESTORE():

        EXCLUDES_FILES = "  "

        if os.path.isfile(FAVS):
                choice2 = xbmcgui.Dialog().yesno(AddonTitle, 'Would you like to keep your Kodi Favourites?', 'Any Favourites included in this build will not', 'be available if you click YES', yeslabel='[COLOR=green]Yes[/COLOR]',nolabel='[COLOR=red]No[/COLOR]')
                if choice2 == 1:
                        EXCLUDES_FILES = "favourites.xml"
                else:
                        EXCLUDES_FILES = "  "

        dp.create(AddonTitle,"Restoring Kodi.",'In Progress...', 'Please Wait')
        try:
                for root, dirs, files in os.walk(HOME,topdown=True):
                        dirs[:] = [d for d in dirs if d not in EXCLUDES]
                        for name in files:
                                if not name == EXCLUDES_FILES:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass
                                else:
                                        continue

                        for name in dirs:
                                try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                except: pass
        except: pass

        dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()

        if os.path.isfile(FAVS):
                FAVS_NEW         =  xbmc.translatePath(os.path.join(USERDATA,'favourites_RESTORE.xml'))
                try:
                        os.rename(FAVS, FAVS_NEW)
                except: pass

        if os.path.exists(NAVI):
                try:
                        shutil.rmtree(NAVI)
                except:
                        pass

        if os.path.exists(DATABASE):
                try:
                        for root, dirs, files in os.walk(DATABASE,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

        if os.path.exists(ADDON_DATA):
                try:
                        for root, dirs, files in os.walk(ADDON_DATA,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

def WIPE_BACKUPRESTORE():

        dp.create(AddonTitle,"Restoring Kodi.",'In Progress...', 'Please Wait')
        try:
                for root, dirs, files in os.walk(HOME,topdown=True):
                        dirs[:] = [d for d in dirs if d not in EXCLUDES]
                        for name in files:
                                try:
                                        os.remove(os.path.join(root,name))
                                        os.rmdir(os.path.join(root,name))
                                except: pass
                        else:
                                continue

                        for name in dirs:
                                try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                except: pass
        except: pass

        dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()

        if os.path.exists(NAVI):
                try:
                        shutil.rmtree(NAVI)
                except:
                        pass

        if os.path.exists(DATABASE):
                try:
                        for root, dirs, files in os.walk(DATABASE,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

        if os.path.exists(ADDON_DATA):
                try:
                        for root, dirs, files in os.walk(ADDON_DATA,topdown=True):
                                dirs[:] = [d for d in dirs]
                                for name in files:
                                        try:
                                                os.remove(os.path.join(root,name))
                                                os.rmdir(os.path.join(root,name))
                                        except: pass

                                for name in dirs:
                                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                                        except: pass
                except: pass

def Check_RD_TRAKT():

        if not os.path.exists(EXCLUDES_FOLDER):
                os.makedirs(EXCLUDES_FOLDER)

        link=Common.OPEN_URL(BASEURL)
        plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
        for match in plugins:
                ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
                ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
                EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))

                if os.path.exists(ADDONSETTINGS):
                        os.rename(ADDONSETTINGS, EXCLUDEMOVE)

def Restore_RD_TRAKT():

        link=Common.OPEN_URL(BASEURL)
        plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
        for match in plugins:
                ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
                ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
                EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
                if os.path.exists(EXCLUDEMOVE):
                        if not os.path.exists(ADDONPATH):
                                os.makedirs(ADDONPATH)
                        if os.path.isfile(ADDONSETTINGS):
                                os.remove(ADDONSETTINGS)
                        os.rename(EXCLUDEMOVE, ADDONSETTINGS)
                        try:
                                os.remove(EXCLUDEMOVE)
                        except: pass

        try:
                shutil.rmtree(EXCLUDEMOVE)
                shutil.rmdir(EXCLUDEMOVE)
        except: pass

        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
        Common.REMOVE_EMPTY_FOLDERS()
