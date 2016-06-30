# This code is licensed under The GNU General Public License version 2 (GPLv2)
# If you decide to fork this code please obey by the licensing rules.
#
# Thanks go to the-one who initially created the initial speedtest code in early 2014
# That code broke but it didn't take too much to fix it, if you get problems it's most likely
# down to the fact that you need to use another download link that plays nicely with XBMC/Kodi

import xbmc, xbmcplugin
import xbmcgui
import xbmcaddon
import urllib
import time
import os
import sys
import datetime

ADDON_ID   = 'plugin.program.sswizard'
ADDON      =  xbmcaddon.Addon(id=ADDON_ID)
HOME       =  ADDON.getAddonInfo('path')
addon_name="Speed Test"
AddonTitle="[COLOR lime]SS[/COLOR] [COLOR cyan]Wizard[/COLOR]"

max_Bps = 0.0
currently_downloaded_bytes = 0.0

#-----------------------------------------------------------------------------------------------------------------
def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle,"Connecting to server",'[COLOR slategray]Testing your internet speed...[/COLOR]', 'Please wait...')
    dp.update(0)
    start_time=time.time()
    try:
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
    except:
        pass    
    return ( time.time() - start_time )
#-----------------------------------------------------------------------------------------------------------------
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        global max_Bps
        global currently_downloaded_bytes
        
        try:
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded_bytes = float(numblocks) * blocksize
            currently_downloaded = currently_downloaded_bytes / (1024 * 1024) 
            Bps_speed = currently_downloaded_bytes / (time.time() - start_time) 
            if Bps_speed > 0:                                                 
                eta = (filesize - numblocks * blocksize) / Bps_speed 
                if Bps_speed > max_Bps: max_Bps = Bps_speed
            else: 
                eta = 0 
            kbps_speed = Bps_speed * 8 / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            dp.update(percent)
        except: 
            currently_downloaded_bytes = float(filesize)
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise Exception("Cancelled")
#-----------------------------------------------------------------------------------------------------------------
def make_dir(mypath, dirname):
    ''' Creates sub-directories if they are not found. '''
    import xbmcvfs
    
    if not xbmcvfs.exists(mypath): 
        try:
            xbmcvfs.mkdirs(mypath)
        except:
            xbmcvfs.mkdir(mypath)
    
    subpath = os.path.join(mypath, dirname)
    
    if not xbmcvfs.exists(subpath): 
        try:
            xbmcvfs.mkdirs(subpath)
        except:
            xbmcvfs.mkdir(subpath)
            
    return subpath
#-----------------------------------------------------------------------------------------------------------------
def GetEpochStr():
    time_now  = datetime.datetime.now()
    epoch     = time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
    epoch_str = str('%f' % epoch)
    epoch_str = epoch_str.replace('.','')
    epoch_str = epoch_str[:-3]
    return epoch_str
#-----------------------------------------------------------------------------------------------------------------
def runtest(url):
    addon_profile_path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    speed_test_files_dir = make_dir(addon_profile_path, 'speedtestfiles')
    speed_test_download_file = os.path.join(speed_test_files_dir, GetEpochStr() + '.speedtest')
    timetaken = download(url, speed_test_download_file)
    os.remove(speed_test_download_file)
    avgspeed = ((currently_downloaded_bytes / timetaken) * 8 / ( 1024 * 1024 ))
    maxspeed = (max_Bps * 8/(1024*1024))
    if avgspeed < 2:
        livestreams = 'Very low quality streams may work.'
        onlinevids = 'Expect buffering, do not try HD.'
        rating = '[COLOR red]Very Poor[/COLOR] | Score: [COLOR slategray]1/10[/COLOR]'
    elif avgspeed < 2.5:
        livestreams = 'You should be ok for SD content only.'
        onlinevids = 'SD/DVD quality should be ok, do not try HD.'
        rating = '[COLOR orange]Poor[/COLOR] | Score: [COLOR slategray]2/10[/COLOR]'
    elif avgspeed < 5:
        livestreams = 'Some HD streams may struggle, SD will be fine.'
        onlinevids = '720p will be fine but some 1080p may struggle.'
        rating = '[COLOR blue]OK[/COLOR] | Score: [COLOR slategray]4/10[/COLOR]'
    elif avgspeed < 9:
        livestreams = 'All streams including HD should stream fine.'
        onlinevids = 'Movies (720p & 1080p) will stream fine but 3D and 4K will struggle.'
        rating = '[COLOR blue]Good[/COLOR] | Score: [COLOR slategray]6/10[/COLOR]'
    elif avgspeed < 15:
        livestreams = 'All streams including HD should stream fine'
        onlinevids = 'Movies (720p & 1080p and 3D) will stream fine but 4K may struggle.'
        rating = '[COLOR green]Very good[/COLOR] | Score: [COLOR slategray]8/10[/COLOR]'
    else:
        livestreams = 'All streams including HD should stream fine'
        onlinevids = 'You can play all movies (720p, 1080p, 3D and 4K)'
        rating = '[COLOR green]Excellent[/COLOR] | Score: [COLOR slategray]10/10[/COLOR]'
    print "Average Speed: " + str(avgspeed)
    print "Max. Speed: " + str(maxspeed)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(
    '[COLOR lightsteelblue]Your Result:[/COLOR] ' + rating,
#    '[COLOR blue]Duration:[/COLOR] %.02f secs' % timetaken,
    '[COLOR lightsteelblue]Live Streams:[/COLOR] ' + livestreams,
    '[COLOR lightsteelblue]Movie Streams:[/COLOR] ' + onlinevids,
	'[COLOR lightsteelblue]Duration:[/COLOR] %.02f secs ' % timetaken + '[COLOR lightsteelblue]Average Speed:[/COLOR] %.02f Mb/s ' % avgspeed + '[COLOR lightsteelblue]Max Speed:[/COLOR] %.02f Mb/s ' % maxspeed,
#    '[COLOR blue]Maximum Speed:[/COLOR] %.02f Mb/s ' % maxspeed,
    )