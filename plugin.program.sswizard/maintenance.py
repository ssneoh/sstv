import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import glob
import common as Common
import downloader

thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.tdbwizard')
mediaPath = os.path.join(addonPath, 'resources/art')
databasePath = xbmc.translatePath('special://userdata/Database')
USERDATA = xbmc.translatePath('special://userdata/')
AddonData = xbmc.translatePath('special://userdata/addon_data')
MaintTitle="[COLOR lime]SS[/COLOR] Maintenance Tools"
EXCLUDES     = ['plugin.program.sswizard','repository.ssneoh.kodi','script.module.addon.common','script.module.requests','temp','kodi.log','kodi.log.old','spmc.log','spmc.log.old']
dp = xbmcgui.DialogProgress()
Windows = xbmc.translatePath('special://home')
WindowsCache = xbmc.translatePath('special://home')
OtherCache = xbmc.translatePath('special://home/temp')
dialog = xbmcgui.Dialog()

#######################################################################
#						Cache Functions
#######################################################################

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi	

#######################################################################
#						Maintenance Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                "special://profile/addon_data/plugin.video.itv/Images"]

    cacheEntries = []

    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))

    return cacheEntries

#######################################################################
#						Clear Cache
#######################################################################

def clearCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log" or f =="kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass

            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass

            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')

        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)

            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')

        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)

            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass    

    cacheEntries = setupCacheEntries()

    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno(MaintTitle,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))

                else:
                    pass


    dialog = xbmcgui.Dialog()
    dialog.ok(MaintTitle, "Done Clearing Cache files")

#######################################################################
#						Delete Thumbnails
#######################################################################

def deleteThumbnails():

    if os.path.exists(thumbnailPath)==True:  
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
            for root, dirs, files in os.walk(thumbnailPath):
                file_count = 0
                file_count += len(files)
                if file_count > 0:                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
    else:
        pass

    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

        dialog.ok("Restart Kodi", "Please restart Kodi to rebuild thumbnail library")

#######################################################################
#						Delete Packages
#######################################################################

def purgePackages():

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "No Packages to Purge")

#######################################################################
#						Convert physical to special
#######################################################################	

def Fix_Special(url):
    HOME         =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(MaintTitle,"Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                dp.update(0,"Fixing","[COLOR yellow]" + file + "[/COLOR]", "Please wait.....")
                a=open((os.path.join(root, file))).read()
                b=a.replace(HOME, 'special://home/')
                f = open((os.path.join(root, file)), mode='w')
                f.write(str(b))
                f.close()

    dialog.ok(MaintTitle, "All physical paths have been converted to special","To complete this process you must force close Kodi now!")
    Common.KillKodi()

#######################################################################
#						Autoclean Function
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                "special://profile/addon_data/plugin.video.itv/Images"]

    cacheEntries = []

    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))

    return cacheEntries

#######################################################################
#						Delete Crash Log Function
#######################################################################

def DeleteCrashLogs():  

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = xbmc.translatePath('special://temp')

    if os.path.exists(HomeDir)==True:   
        dialog = xbmcgui.Dialog()
        if dialog.yesno(MaintTitle, '', "Do you want to delete old crash logs?"):
            path=Windows
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)

            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(WindowsCache)==True:   
            path=WindowsCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)

            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OtherCache)==True:   
            path=OtherCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)

            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        dialog = xbmcgui.Dialog()
        dialog.ok(MaintTitle, "Crash logs deleted", "[COLOR yellow]Thank you for using SS Wizard[/COLOR]")

    else:

        dialog = xbmcgui.Dialog()
        dialog.ok(MaintTitle, "An error occured", "[COLOR yellow]Please try again later[/COLOR]")

def viewLogFile():
    kodilog = xbmc.translatePath('special://logpath/kodi.log')
    spmclog = xbmc.translatePath('special://logpath/spmc.log')
    kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
    spmcold = xbmc.translatePath('special://logpath/spmc.old.log')

    if os.path.exists(spmclog):
        if os.path.exists(spmclog) and os.path.exists(spmcold):
            choice = xbmcgui.Dialog().yesno(MaintTitle,"Curretn & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
            if choice == 0:
                f = open(spmclog,mode='r'); msg = f.read(); f.close()
                Common.TextBoxes("%s - spmc.log" % msg)
            else:
                f = open(spmcold,mode='r'); msg = f.read(); f.close()
                Common.TextBoxes("%s - spmc.old.log" % msg)
        else:
            f = open(spmclog,mode='r'); msg = f.read(); f.close()
            Common.TextBoxes("%s - spmc.log" % msg)

    if os.path.exists(kodilog):
        if os.path.exists(kodilog) and os.path.exists(kodiold):
            choice = xbmcgui.Dialog().yesno(MaintTitle,"Curretn & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
            if choice == 0:
                f = open(kodilog,mode='r'); msg = f.read(); f.close()
                Common.TextBoxes("%s - kodi.log" % msg)
            else:
                f = open(kodiold,mode='r'); msg = f.read(); f.close()
                Common.TextBoxes("%s - kodi.old.log" % msg)
        else:
            f = open(kodilog,mode='r'); msg = f.read(); f.close()
            Common.TextBoxes("%s - kodi.log" % msg)

    if os.path.isfile(kodilog) or os.path.isfile(spmclog):
        return True
    else:
        dialog.ok(MaintTitle,'Sorry, No log file was found.','','[COLOR yellow]Thank you for using SS Wizard[/COLOR]')

def autocleanask():

    choice = xbmcgui.Dialog().yesno(MaintTitle, 'Selecting [COLOR green]YES[/COLOR] will delete your cache, thumbnails and packages.','[I][COLOR lightsteelblue]Do you wish to continue?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
    if choice == 1:
        autocleannow()

def autocleannow():
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        if (f == "xbmc.log" or f == "xbmc.old.log" or f =="kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

            else:
                pass

    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        if (f == "kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')

        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)

            if file_count > 0:                
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')

        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)

            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

            else:
                pass    

    cacheEntries = setupCacheEntries()

    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

                else:
                    pass

    if os.path.exists(thumbnailPath)==True:  
        for root, dirs, files in os.walk(thumbnailPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:                
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
    else:
        pass

    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
        if file_count > 0:            
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    choice = xbmcgui.Dialog().yesno(MaintTitle,"Auto clean finished.","Your cache, thumbnails and packages have all been deleted","[I][COLOR lightsteelblue]Do you want to restart your device now to finish the process?[/COLOR][/I]", yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
    if choice == 1:
        Common.KillKodi()

def autocleanask():

    choice = xbmcgui.Dialog().yesno(MaintTitle, 'Selecting [COLOR green]YES[/COLOR] will delete your cache, thumbnails and packages.','[I][COLOR lightsteelblue]Do you wish to continue?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
    if choice == 1:
        autocleannow()

def AutoCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        if (f == "xbmc.log" or f == "xbmc.old.log" or f =="kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

            else:
                pass

    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        if (f == "kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')

        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)

            if file_count > 0:                
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')

        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)

            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

            else:
                pass    

    cacheEntries = setupCacheEntries()

    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

                else:
                    pass

def AutoThumbs():

    if os.path.exists(thumbnailPath)==True:  
        for root, dirs, files in os.walk(thumbnailPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:                
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
    else:
        pass

    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

def AutoPackages():

    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
        if file_count > 0:            
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

def AutoCrash():  

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = xbmc.translatePath('special://temp')

    if os.path.exists(HomeDir)==True:   
        path=Windows
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)

        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)

    if os.path.exists(WindowsCache)==True:   
        path=WindowsCache
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)

        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)

    if os.path.exists(OtherCache)==True:   
        path=OtherCache
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)

        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)