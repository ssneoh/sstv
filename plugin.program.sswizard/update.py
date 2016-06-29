import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import re
import glob
import extract
import plugintools
import downloader
import time
import common as Common
import wipe
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
        version = 'TheWizardIsHere'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open
AddonTitle="[COLOR lime]SS[/COLOR] Wizard"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

SSOne = "http://pastebin.com/raw/85Ct9Jfi"
SSTwo = "http://pastebin.com/raw/d1DjeFSL"

############################
###CHECK FOR UPDATES########
############################

def updateaddons():

        xbmc.executebuiltin( "ActivateWindow(busydialog)" )
        xbmc.executebuiltin('UpdateAddonRepos()')
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        if not os.path.exists(CHECKVERSION):
                dialog.ok(AddonTitle,'[COLOR ghostwhite]All repositories have been checked for updates.[/COLOR]','[COLOR powderblue]All available addon updates have now been installed.[/COLOR]','')
                sys.exit(1)
        choice = xbmcgui.Dialog().yesno(AddonTitle,'[COLOR ghostwhite]All repositories have been checked for updates.[/COLOR]','[COLOR powderblue]All available addon updates have now been installed.[/COLOR]','[COLOR yellow]Check for build updates now?[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
        if choice == 1:
                check()
        else:
                sys.exit(1)

def check():

        xbmc.executebuiltin( "ActivateWindow(busydialog)" )
        pleasecheck = 0
        SSUpdate = 0
        dialog = xbmcgui.Dialog()

        try:
                response = urlopen(SSTwo)
        except:
                SSUpdate = 1
                dialog.ok(AddonTitle,'Sorry we are unable to check for [B]SS TV[/B] updates!','The update host appears to be down.','')
                xbmc.executebuiltin( "Dialog.Close(busydialog)" )


#######################################################################
#						Check for Build Updates
#######################################################################

        if SSUpdate == 0 and os.path.isfile(CHECKVERSION):
                dialog = xbmcgui.Dialog()
                checkurl = SSTwo
                vers = open(CHECKVERSION, "r")
                regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
                for line in vers:
                        if SSUpdate == 0:
                                currversion = regex.findall(line)
                                for build,vernumber in currversion:
                                        if vernumber > 0:
                                                req = urllib2.Request(checkurl)
                                                req.add_header('User-Agent','TheWizardIsHere')
                                                try:
                                                        response = urllib2.urlopen(req)
                                                except:
                                                        dialog.ok(AddonTitle,'Sorry we are unable to check for [B]SS TV[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')
                                                        sys.exit(1)		
                                                        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                                link=response.read()
                                                response.close()
                                                match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
                                                for newversion,fresh in match:
                                                        if newversion > vernumber:
                                                                choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
                                                                if choice == 1: 
                                                                        if fresh =='false': # TRUE
                                                                                updateurl = SSOne
                                                                                req = urllib2.Request(updateurl)
                                                                                req.add_header('User-Agent','TheWizardIsHere')
                                                                                try:
                                                                                        response = urllib2.urlopen(req)
                                                                                except:
                                                                                        dialog.ok(AddonTitle,'Sorry we were unable to download the update!','The update host appears to be down.','Please check for updates later via the wizard.')
                                                                                        sys.exit(1)	
                                                                                        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
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
                                                                                        print '======================================='
                                                                                        print addonfolder
                                                                                        print '======================================='
                                                                                        extract.all(lib,addonfolder,dp)
                                                                                        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                                                                        dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")

                                                                                        Common.killxbmc()
                                                                                        sys.exit(1)		

                                                                        else:
                                                                                dialog.ok(AddonTitle,'[COLOR red]A WIPE (FACTORY RESET)[/COLOR] is required for the update... [COLOR red]WOULD YOU LIKE TO WIPE THE SYSTEM NOW?[/COLOR]','','')
                                                                                xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                                                                wipe.FRESHSTART()
                                                                                sys.exit(1)	
                                                                else:
                                                                        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                                                        sys.exit(1)												
                                                        else:
                                                                xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                                                                dialog.ok(AddonTitle,'[COLOR ghostwhite]Your build is up to date.[/COLOR]', "[COLOR ghostwhite]Current Build: [/COLOR][COLOR yellow]" + build + "[/COLOR]", "[COLOR ghostwhite]Current Version: [/COLOR][COLOR yellow]" + newversion + "[/COLOR]")
                                                                sys.exit(1)		


        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        dialog.ok(AddonTitle,'[COLOR ghostwhite]An unknown error occurred.[/COLOR]', "[COLOR yellow]Please try again later.[/COLOR]", "")
