#!/usr/bin/env python2.7

from HTMLParser import HTMLParser
import time
import sys, os, imp
import subprocess
import urllib2

try:
	import twitter
except ImportError:
	pass

tokensurl = "TOKENS_FILE_HERE"
scriptdir = os.path.dirname(os.path.realpath(__file__))
cachedir = os.path.join(scriptdir, "cache")
lasttweet = ""

if not os.path.exists(cachedir):
	os.makedirs(cachedir)

def printlog(log):
	logtime = time.strftime("[%a %b %d %H:%M:%S %Z %Y]")
	log = logtime + " [autopro] " + log
	print log

def readpage(url):
	printlog("Connecting to %s..." % url)

	retry = {}
	retry['count'] = 0
	retry['max'] = 5

	page = None
	while not page and retry['count'] <= retry['max']:
		retry['count'] += 1
		try: # connect to page
			page = urllib2.urlopen(url) # open url
			page = page.read()
			printlog("Connection successful.")
		except Exception, e: # if fails, retry
			printlog("Connection failed: %s (retrying in 30 seconds)" % e[0]['message'])
			time.sleep(30)
			printlog("Retrying... (%s retries left)" % retry['max'] - retry['count'])

	if not page:
		printlog("Connection failed after %s retries. Please check your internet connection. Exiting..." % retry['count'])
		sys.exit(1)

	return page

def unescape(str):
	str = str.decode('utf-8')
	str = HTMLParser().unescape(str)
	str = str.encode('utf-8')
	return str

def verbfix(html):
	verbs = {
		"has"	: "have",
		"their"	: "my"
	}

	for v in verbs:
		html = html.replace(v, verbs[v])

	return html

def htmltotext(html):
	valtags = ["a", "img"]
	tags = ["</a>", "<b>", "</b>", "<ul>", "</ul>", "<li>", "</li>"]

	# remove tags
	for t in tags:
		html = html.replace(t, "")

	# remove tags with values
	for vt in valtags:
		str = "<%s" % vt
		while html.find(str) > -1:
			start = html.find(str)
			end = html.find(">", start) + 1
			html = html.replace(html[start:end], "")

	html = html.strip()

	return html

def posttweet(tweet, access_key, access_secret):
	api_twitter = twitter.Api(consumer_key='CONSUMER_KEY_HERE', 
	consumer_secret='CONSUMER_SECRET_HERE',
	access_token_key=access_key,
	access_token_secret=access_secret)

	printlog("Tweeting \"%s\"..." % tweet)

	if len(tweet) > 140:
		return printlog("Tweet is longer than 140 characters. Aborted.")

	if tweet == lasttweet:
		return printlog("Tweet is a duplicate. Aborted.")

	retry = {}
	retry['count'] = 0
	retry['max'] = 5

	posted = None
	while not posted and retry['count'] <= retry['max']:
		retry['count'] += 1
		try: # post tweet
			posted = api_twitter.PostUpdate(tweet)
			printlog("Tweet posted.")
		except Exception, e: # if fails, retry
			printlog("Failed to post tweet: %s (retrying in 30 seconds)" % e[0]['message'])
			time.sleep(30)
			printlog("Retrying... (%s retries left)" % retry['max'] - retry['count'])

	if not posted:
		printlog("Failed to post tweet after %s retries. Aborted." % retry['count'])

def cutstring(string, sstring1, sstring2):
	start = string.find(sstring1) + len(sstring1)
	end = string.find(sstring2, start)
	return string[start:end]

def printpid():
	fn = os.path.basename(__file__)
	fn = fn.replace(".py", ".pid")
	with open(fn, 'w') as f:
		f.write(str(os.getpid()))
		f.close()

def main():
	tokens = readpage(tokensurl)
	tokens = unescape(tokens)
	tokens = tokens.split("\n")

	database = []
	for line in tokens:
		line = line.strip()
		if line:
			parts = line.split()
			database.append(parts)

	caches = {}
	for fn in os.listdir(cachedir):
		userid = fn.replace(".db", "")
		caches[userid] = False

	for keys in database:
		data = []

		userid = keys[0]
		access_key = keys[1]
		access_secret = keys[2]

		# cache validation
		if userid in caches:
			caches[userid] = True

		# open the profile
		page = readpage("http://osu.ppy.sh/pages/include/profile-general.php?u=%s" % userid)
		page = unescape(page)

		# find div containing the activites
		activity = cutstring(page, "<div id='full'", "<div class='profileStatHeader'")

		# gather all the data first
		recents = activity.split("<tr>")[1:]
		for r in reversed(recents):
			# find timestamp
			timestamp = cutstring(r, "datetime='", "'>")
			# find activity
			activity = cutstring(r, "</b>", "</div>")
			activity = htmltotext(activity)
			activity = verbfix(activity)
			# append to data
			data.append([timestamp, activity])

		fn = os.path.join(cachedir, userid + ".db")
		if os.path.exists(fn): # this user has no cache yet
			with open(fn, 'r') as f: # read the cache first
				cache = []
				for line in f:
					line = line.strip()
					if line:
						parts = line.split(None, 1)
						cache.append([parts[0], parts[1]])
				f.close()

			with open(fn, 'a') as f: # append new activites to cache
				for a in data:
					if not a in cache:
						f.write("%s %s\n" % (a[0], a[1]))
						tweet = "I %s #osuautorecent http://bit.ly/16iJoqO" % a[1]
						posttweet(tweet, access_key, access_secret)
				f.close()
		else:
			with open(fn, 'w') as f:
				for a in data:
					f.write("%s %s\n" % (a[0], a[1]))
				f.close()
			printlog("Created %s" % fn)

	# invalid cache removal
	for userid in caches:
		if not caches[userid]:
			fn = os.path.join(cachedir, userid + ".db")
			printlog("Removed %s" % fn)
			os.remove(fn)

	printlog("Exited successfully.")

if __name__ == '__main__':
	printpid()
	main()
