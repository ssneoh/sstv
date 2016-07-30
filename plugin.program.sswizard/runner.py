import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import base64
import time
import downloader
import zipfile
import common as Common

SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.sswizard',''))
REPO     =  xbmc.translatePath(os.path.join('special://home/addons','repository.ssneoh.kodi'))
WIZARD     =  xbmc.translatePath(os.path.join('special://home/addons','plugin.program.sswizard'))
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"
InstallRepo = 'https://www.dropbox.com/s/662cbsctj6l5cfb/repository.ssneoh.kodi-1.0.0.zip?dl=1'

def check():

	if not os.path.exists(REPO):
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'The SS Repository is not installed','It is a requirement of the SS Wizard to have the repo installed.','Do you want to install the SS Repository now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			INSTALL()
		else:
			sys.exit(0)

def INSTALL():

	url = InstallRepo
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)

	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Installing Repository")
	lib=os.path.join(path, 'repo.zip')
		
	try:
		os.remove(lib)
	except:
		pass
	
	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass


	dialog.ok(AddonTitle, "SS Repository successfully installed")
	
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