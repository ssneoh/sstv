import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
import time
import downloader
import common as Common
import wipe
import zipfile
import hashlib
import skinSwitch

AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
skin         =  xbmc.getSkinDir()
KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
FAVS_NEW         =  xbmc.translatePath(os.path.join(USERDATA,'favourites_RESTORE.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))

############################
###INSTALL BUILD############
############################

def INSTALL(name,url,description):

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	
	wipeme = 1
	skipskin = 0

	skin         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	skinswapped = 0

	#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary'] and skipskin == 0:
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
	if skin not in ['skin.confluence','skin.estuary'] and skipskin == 0:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR red]Click YES to MANUALLY SWITCH the skin now[/COLOR]','[COLOR red]You can press NO and attempt the AUTO SWITCH again if you wish[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			xbmc.executebuiltin("ActivateWindow(appearancesettings)")
			return
		else:
			sys.exit(1)

	if wipeme == 1:
		wipe.WIPERESTORE()

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Build: " + buildname)
	name = "build"
	lib=os.path.join(path, name+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass
	
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	unzip(lib,addonfolder,dp)
	dialog = xbmcgui.Dialog()
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass

	if os.path.isfile(FAVS_NEW):
		if os.path.isfile(FAVS):
			try:
				os.remove(FAVS)
				os.rename(FAVS_NEW, FAVS)
			except: pass
		else:
			try:
				os.rename(FAVS_NEW, FAVS)
			except: pass

	dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
	Common.killxbmc()

def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Extraction was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True