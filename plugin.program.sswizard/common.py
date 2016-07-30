import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
from urllib2 import urlopen
import extract
import downloader
import re
import time
addon_id = 'plugin.program.sswizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.sswizard'
HOME         =  xbmc.translatePath('special://home/')
dialog       =  xbmcgui.Dialog()
BASEURL = 'http://ssneoh.site88.net'


#######################################################################
#						Add to menus
#######################################################################

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addItem(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirWTW(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name, url, mode, iconimage):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
                + "&name=" + urllib.quote_plus(name)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                               thumbnailImage=iconimage)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                         listitem=liz, isFolder=False)
        return ok

#######################################################################
#				INDIVIDUAL BUILDS MENU
#######################################################################

#def BUILDER(name,url,iconimage,fanart,description):

        #urla = url
        #url = str(name + "," + urla)
        #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
        #body = urllib2.urlopen(service_url).read()

        #addDir("[COLOR orangered][B]Download The Build[/COLOR][/B]",url,90,iconimage,fanart,description)
        #url = name
        #addItem("[COLOR white][B]Write A Review[/COLOR][/B]",url,58,iconimage,fanart,description)
        #addDir("[COLOR white][B]Read All Reviews - (Total: " + body + " Reviews)[/COLOR][/B]",url,59,iconimage,fanart,description)

#def BUILDER_COMMUNITY(name,url,iconimage,fanart,description):

        #urla = url
        #url = str(name + "," + urla)
        #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
        #body = urllib2.urlopen(service_url).read()

        #addDir("[COLOR orangered][B]Download The Build[/COLOR][/B]",url,96,iconimage,fanart,description)
        #url = name
        #addItem("[COLOR white][B]Write A Review[/COLOR][/B]",url,58,iconimage,fanart,description)
        #addDir("[COLOR white][B]Read All Reviews - (Total: " + body + " Reviews)[/COLOR][/B]",url,59,iconimage,fanart,description)

#def WriteReview(build_name):

        #review_text =''
        #name_text = ''
        #review_ip = urlopen('http://ip.42.pl/raw').read()

        #try:
                #Review_keyboard = xbmc.Keyboard(review_text, 'Enter Your Review')
                #Review_keyboard.doModal()

                #if Review_keyboard.isConfirmed():
                        #review_text = Review_keyboard.getText()
                        #Review_Name = xbmc.Keyboard(name_text, 'Enter Your Name')
                        #Review_Name.doModal()

                #if Review_Name.isConfirmed():
                        #name_text = Review_Name.getText()

                #if 	review_text == "":
                        #dialog.ok('TDB Reviews', "[B][COLOR powderblue]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR powderblue]Please try again.[/COLOR][/B]", '')
                        #sys.exit(1)

                #if 	name_text == "":
                        #dialog.ok('TDB Reviews', "[B][COLOR powderblue]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR powderblue]Please try again.[/COLOR][/B]", '')
                        #sys.exit(1)

                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1hZGQmdGV4dD0=') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except: sys.exit(1)

        #dialog.ok('TDB Reviews', "[B][COLOR powderblue]Thanks, For leaving A Review for : [/COLOR][/B]", "", build_name )

#def ListReview(build_name):

        #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1yZWFkJmJ1aWxkPQ==') + base64.b64encode(build_name)
        #f = urllib2.urlopen(service_url)
        #data = f.read()
        #f.close()

        #reviews = review_parse(data)
        #xbmc.log("got review parse : "+data)
        #for review in reviews:
                #review_title = "[COLOR blue][B]"+review['date']+"[/COLOR][/B] - [COLOR white][B] Read Review By : " +review['name']+ "[/COLOR][/B]"
                #url = review['review']
                #date = "Review Date : " + review['date']
                #xbmc.log(review['name']+" : "+review['date'])

                #addItem(review_title,url,49,'date','','')


#def review_parse(data):

        #patron = "<item>(.*?)</item>"
        #reviews = re.findall(patron,data,re.DOTALL)

        #items = []
        #for review in reviews:
                #item = {}
                #item["name"] = find_single_match(review,"<name>([^<]+)</name>")
                #item["date"] = find_single_match(review,"<date>([^<]+)</date>")
                #item["review"] = find_single_match(review,"<review>([^<]+)</review>")

                #if item["name"]!="":
                        #items.append(item)

        #return items

#def add_one(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0016[/COLOR][/B]")
        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV90b3RhbC5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0017[/COLOR][/B]")

#def add_one_community(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHkucGhwP2FjdGlvbj1hZGQmbmFtZT0=') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0018[/COLOR][/B]")

#def add_one_advanced(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZHZhbmNlZC5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0019[/COLOR][/B]")

#def add_one_backups(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9iYWNrdXBzLnBocD9hY3Rpb249YWRkJm5hbWU9') + base64.b64encode(build_name)
                #body =urllib2.urlopen(service_url).read()
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0020[/COLOR][/B]")

#def count(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
                #f = urllib2.urlopen(service_url)
                #data = f.read()
                #f.close()

                #return data
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0021[/COLOR][/B]")

#def count_total(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV90b3RhbC5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
                #f = urllib2.urlopen(service_url)
                #data = f.read()
                #f.close()

                #return data
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0022[/COLOR][/B]")

#def count_community(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHkucGhwP2FjdGlvbj1jb3VudCZuYW1lPQ==') + base64.b64encode(build_name)
                #f = urllib2.urlopen(service_url)
                #data = f.read()
                #f.close()

                #return data
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0023[/COLOR][/B]")

#def count_advanced(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZHZhbmNlZC5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
                #f = urllib2.urlopen(service_url)
                #data = f.read()
                #f.close()

                #return data
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0024[/COLOR][/B]")

#def count_backups(build_name):

        #try:
                #service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9iYWNrdXBzLnBocD9hY3Rpb249Y291bnQmbmFtZT0=') + base64.b64encode(build_name)
                #f = urllib2.urlopen(service_url)
                #data = f.read()
                #f.close()

                #return data
        #except:
                #dialog.ok(AddonTitle, "[B][COLOR powderblue]Sorry, TDB Wizard encountered an error[/COLOR][/B]",'[COLOR yellow]Please report the error code at tdbwizard.co.uk.[/COLOR]',"[B][COLOR white]Error Code:[/COLOR][COLOR red] 0025[/COLOR][/B]")

#def find_single_match(text,pattern):

        #result = ""
        #try:    
                #single = re.findall(pattern,text, flags=re.DOTALL)
                #result = single[0]
        #except:
                #result = ""

        #return result

def _get_keyboard( default="", heading="", hidden=False ):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard( default, heading, hidden )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
                return unicode( keyboard.getText(), "utf-8" )
        return default

def TextBoxes(announce):
        class TextBox():
                WINDOW=10147
                CONTROL_LABEL=1
                CONTROL_TEXTBOX=5
                def __init__(self,*args,**kwargs):
                        xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
                        self.win=xbmcgui.Window(self.WINDOW) # get window
                        xbmc.sleep(500) # give window time to initialize
                        self.setControls()
                def setControls(self):
                        self.win.getControl(self.CONTROL_LABEL).setLabel('SS Wizard - View Log Facility') # set heading
                        try: f=open(announce); text=f.read()
                        except: text=announce
                        self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
                        return
        TextBox()
        while xbmc.getCondVisibility('Window.IsVisible(10147)'):
                time.sleep(.5)

def TextBoxesPlain(announce):
        class TextBox():
                WINDOW=10147
                CONTROL_LABEL=1
                CONTROL_TEXTBOX=5
                def __init__(self,*args,**kwargs):
                        xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
                        self.win=xbmcgui.Window(self.WINDOW) # get window
                        xbmc.sleep(500) # give window time to initialize
                        self.setControls()
                def setControls(self):
                        self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR powderblue][B]SS Wizard[/B][/COLOR]') # set heading
                        try: f=open(announce); text=f.read()
                        except: text=announce
                        self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
                        return
        TextBox()
        while xbmc.getCondVisibility('Window.IsVisible(10147)'):
                time.sleep(.5)

def OPEN_URL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'TheWizardIsHere')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link  

def OPEN_URL_NORMAL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link  

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
        return s

##########################
###DETERMINE PLATFORM#####
##########################

def platform():
        if xbmc.getCondVisibility('system.platform.android'):
                return 'android'
        elif xbmc.getCondVisibility('system.platform.linux'):
                return 'linux'
        elif xbmc.getCondVisibility('system.platform.windows'):
                return 'windows'
        elif xbmc.getCondVisibility('system.platform.osx'):
                return 'osx'
        elif xbmc.getCondVisibility('system.platform.atv2'):
                return 'atv2'
        elif xbmc.getCondVisibility('system.platform.ios'):
                return 'ios'

############################
###REMOVE EMPTY FOLDERS#####
############################

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
        print"########### Start Removing Empty Folders #########"
        empty_count = 0
        used_count = 0
        for curdir, subdirs, files in os.walk(HOME):
                if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
                        empty_count += 1 #increment empty_count
                        os.rmdir(curdir) #delete the directory
                        print "successfully removed: "+curdir
                elif len(subdirs) > 0 and len(files) > 0: #check for used directories
                        used_count += 1 #increment 

###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
        dialog       =  xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno('[COLOR=lightsteelblue]Force Close Kodi[/COLOR]', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='[COLOR=green]Yes, Close[/COLOR]')
        if choice == 0:
                return
        elif choice == 1:
                pass
        myplatform = platform()
        print "Platform: " + str(myplatform)
        if myplatform == 'osx': # OSX
                print "############   try osx force close  #################"
                try: os.system('killall -9 XBMC')
                except: pass
                try: os.system('killall -9 Kodi')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
        elif myplatform == 'linux': #Linux
                print "############   try linux force close  #################"
                try: os.system('killall XBMC')
                except: pass
                try: os.system('killall Kodi')
                except: pass
                try: os.system('killall -9 xbmc.bin')
                except: pass
                try: os.system('killall -9 kodi.bin')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
        elif myplatform == 'android': # Android  
                print "############   try android force close  #################"
                try: os.system('adb shell am force-stop org.xbmc.kodi')
                except: pass
                try: os.system('adb shell am force-stop org.kodi')
                except: pass
                try: os.system('adb shell am force-stop org.xbmc.xbmc')
                except: pass
                try: os.system('adb shell am force-stop org.xbmc')
                except: pass     
                try: os.system('adb shell am force-stop com.semperpax.spmc16')
                except: pass
                try: os.system('adb shell am force-stop com.spmc16')
                except: pass      		
                try: os.system('adb shell am force-stop com.semperpax.spmc')
                except: pass
                try: os.system('adb shell am force-stop com.spmc')
                except: pass    
                try: os.system('adb shell am force-stop uk.droidbox.dbmc')
                except: pass
                try: os.system('adb shell am force-stop uk.dbmc')
                except: pass   
                try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
                except: pass
                try: os.system('adb shell am force-stop com.jesusboxmedia')
                except: pass 
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
        elif myplatform == 'windows': # Windows
                print "############   try windows force close  #################"
                try:
                        os.system('@ECHO off')
                        os.system('tskill XBMC.exe')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('tskill Kodi.exe')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('TASKKILL /im Kodi.exe /f')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('TASKKILL /im XBMC.exe /f')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
        else: #ATV
                print "############   try atv force close  #################"
                try: os.system('killall AppleTV')
                except: pass
                print "############   try raspbmc force close  #################" #OSMC / Raspbmc
                try: os.system('sudo initctl stop kodi')
                except: pass
                try: os.system('sudo initctl stop xbmc')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    


def KillKodi():
        myplatform = platform()
        print "Platform: " + str(myplatform)
        if myplatform == 'osx': # OSX
                print "############   try osx force close  #################"
                try: os.system('killall -9 XBMC')
                except: pass
                try: os.system('killall -9 Kodi')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
        elif myplatform == 'linux': #Linux
                print "############   try linux force close  #################"
                try: os.system('killall XBMC')
                except: pass
                try: os.system('killall Kodi')
                except: pass
                try: os.system('killall -9 xbmc.bin')
                except: pass
                try: os.system('killall -9 kodi.bin')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
        elif myplatform == 'android': # Android  
                print "############   try android force close  #################"
                try: os.system('adb shell am force-stop org.xbmc.kodi')
                except: pass
                try: os.system('adb shell am force-stop org.kodi')
                except: pass
                try: os.system('adb shell am force-stop org.xbmc.xbmc')
                except: pass
                try: os.system('adb shell am force-stop org.xbmc')
                except: pass     
                try: os.system('adb shell am force-stop com.semperpax.spmc16')
                except: pass
                try: os.system('adb shell am force-stop com.spmc16')
                except: pass      		
                try: os.system('adb shell am force-stop com.semperpax.spmc')
                except: pass
                try: os.system('adb shell am force-stop com.spmc')
                except: pass    
                try: os.system('adb shell am force-stop uk.droidbox.dbmc')
                except: pass
                try: os.system('adb shell am force-stop uk.dbmc')
                except: pass   
                try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
                except: pass
                try: os.system('adb shell am force-stop com.jesusboxmedia')
                except: pass 
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
        elif myplatform == 'windows': # Windows
                print "############   try windows force close  #################"
                try:
                        os.system('@ECHO off')
                        os.system('tskill XBMC.exe')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('tskill Kodi.exe')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('TASKKILL /im Kodi.exe /f')
                except: pass
                try:
                        os.system('@ECHO off')
                        os.system('TASKKILL /im XBMC.exe /f')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
        else: #ATV
                print "############   try atv force close  #################"
                try: os.system('killall AppleTV')
                except: pass
                print "############   try raspbmc force close  #################" #OSMC / Raspbmc
                try: os.system('sudo initctl stop kodi')
                except: pass
                try: os.system('sudo initctl stop xbmc')
                except: pass
                dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    