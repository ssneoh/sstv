import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import zipfile
import extract
import downloader
import installer
import re
import time
import common as Common
import wipe
import plugintools
from random import randint
from datetime import date
import calendar
import maintenance

def Checker():

	addon_id = 'plugin.program.sswizard'
	my_date = date.today()
	today = calendar.day_name[my_date.weekday()]
	accache = plugintools.get_setting("accache")
	acpackages = plugintools.get_setting("acpackages")
	accrash = plugintools.get_setting("accrash")
	acthumbs = plugintools.get_setting("acthumbs")
	acmonday = plugintools.get_setting("acmonday")
	actuesday = plugintools.get_setting("actuesday")
	acwednesday = plugintools.get_setting("acwednesday")
	acthursday = plugintools.get_setting("acthursday")
	acfriday = plugintools.get_setting("acfirday")
	acsaturday = plugintools.get_setting("acsaturday")
	acsinday = plugintools.get_setting("acsunday")
	cleaned = 0
	CLEANEDTODAY = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedtoday.txt'))

	if today == "Monday" and acmonday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')

	if today == "Tuesday" and actuesday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')
		
	if today == "Wednesday" and acwednesday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')

	if today == "Thursday" and acthursday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')

	if today == "Friday" and acfriday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')

	if today == "Saturday" and acsaturday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')
		
	if today == "Sunday" and acsunday == "true":
		cleaned = 1
		if not os.path.isfile == CLEANEDTODAY:
			if accache == "true":
				maintenance.AutoCache()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			open(CLEANEDTODAY, 'w')

	if cleaned == 0:
		if os.path.isfile(CLEANEDTODAY):
			os.remove(CLEANEDTODAY)
