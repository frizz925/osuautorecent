#!/usr/bin/env python2.7
# base module containing basic functions

from HTMLParser import HTMLParser
import os, sys, time
import urllib2, json, codecs

class Functions(object): # class for functions that handle with local files	class Twitter(object): # class for handling with Twitter API
	class Twitter(object):
		def __init__(self, funcs, keys):
			self.funcs = funcs
			# try loading Twitter module
			try:
				import twitter as twitterAPI
				self.api_twitter = twitterAPI.Api(consumer_key=keys[0], consumer_secret=keys[1], access_token_key=keys[2], access_token_secret=keys[3])
			except ImportError:
				self.api_twitter = None
		
			self.lasttweet = ""
	
		def PostTweet(self, tweet, prefix="", suffix=""):
			if not self.api_twitter:
				return self.funcs.printlog("Cannot post tweet. Twitter module is missing.")
			if tweet == self.lasttweet:
				return self.funcs.printlog("Tweet is a duplicate. Aborted.")
	
			# tweet shortening
			if len(prefix) + len(tweet) + len(suffix) > 140:
				maxchars = 135 - len(suffix) - len(prefix)
				tweet = tweet[:maxchars] + "..."

			tweet = prefix + " " + tweet + " " + suffix
			tweet = tweet.strip()
			self.funcs.printlog("Tweeting \"%s\"..." % tweet)
		
			retry = {}
			retry['max'] = 5
			retry['count'] = retry['max']
		
			posted = None
			while not posted and retry['count'] > 0:
				retry['count'] -= 1
				try: # post tweet
					posted = self.api_twitter.PostUpdate(tweet)
					self.lasttweet = tweet
					self.funcs.printlog("Tweet posted.")
				except Exception, e: # if fails, retry
					self.funcs.printlog("Failed to post tweet: %s (retrying in 30 seconds)" % e)
					time.sleep(30)
					self.funcs.printlog("Retrying... (%s retries left)" % retry['count'])
		
			if not posted:
				self.funcs.printlog("Failed to post tweet after %s retries. Aborted." % retry['max'])

			# timeout for 5 secs
			time.sleep(5)

	def twitter(self, keys):
		return self.Twitter(self, keys)

	class File(object): # ayadayada this class is stupidly useless but whatever
		def __init__(self, funcs, fn):
			self.wasEmpty = False
			self.funcs = funcs
			self.fn = fn
	
		def WarnNotExist(self):
			fn = os.path.basename(self.fn)
			self.funcs.printlog(fn + " does not exist.")
	
		def CheckFile(self):
			if not os.path.exists(self.fn):
				return False
			return True

		def ReadToString(self):
			if self.CheckFile():
				result = ""
				with codecs.open(self.fn, 'r', 'utf-8') as f:
					for line in f:
						result += line
					f.close()
				return result
			else:
				self.WarnNotExist()
				return None
	
		def ReadToList(self):
			if self.CheckFile():
				result = []
				with codecs.open(self.fn, 'r', 'utf-8') as f:
					for line in f:
						line = line.strip()
						if line:
							result.append(line)
					f.close()
				return result
			else:
				self.WarnNotExist()
				return None
	
		def Write(self, string):
			with codecs.open(self.fn, 'w', 'utf-8') as f:
				f.write(string)
				f.close()
	
		def Append(self, string):
			if not self.CheckFile():
				self.Write(string)
			else:
				with codecs.open(self.fn, 'a', 'utf-8') as f:
					f.write(string)
					f.close()

		def AppendLine(self, string):
			self.Append(string + "\n")

	def file(self, fn):
		return self.File(self, fn)

	def __init__(self, script):
		self.scriptdir = os.path.dirname(os.path.realpath(script))
		self.scriptfn = os.path.basename(script)
		self.jsonfn = self.scriptfn.replace(".py", ".json")
		self.pidfn = self.scriptfn.replace(".py", ".pid")

	def printlog(self, log):
		logtime = time.strftime("[%a %b %d %H:%M:%S %Z %Y]")
		module = self.scriptfn.replace(".py", "")
		log = "%s [%s] %s" % (logtime, module, log)
		print log

	def printpid(self): # this may come in handy for scheduled task killing
		fn = os.path.join(self.scriptdir, self.pidfn)
		with open(fn, 'w') as f:
			f.write(str(os.getpid()))
			f.close()

	def decodelocaljson(self, key=None): # decode local json file containing keys
		fn = os.path.join(self.scriptdir, self.jsonfn)
		if not os.path.exists(fn): # json file missing
			print self.jsonfn + " not found. Please create one."
			sys.exit(1)

		with open(fn) as f:
			json_output = json.load(f)
			if key:
				json_output = json_output[key]
			f.close()

		return json_output

	def readpage(self, url):
		self.printlog("Connecting to %s..." % url)
	
		retry = {}
		retry['max'] = 5
		retry['count'] = retry['max']
	
		page = None
		while not page and retry['count'] > 0:
			retry['count'] -= 1
			try: # connect to page
				page = urllib2.urlopen(url) # open url
				page = page.read()
				self.printlog("Connection successful.")
			except Exception, e: # if fails, retry
				self.printlog("Connection failed: %s (retrying in 30 seconds)" % e)
				time.sleep(30)
				self.printlog("Retrying... (%s retries left)" % retry['count'])
	
		if not page:
			funcs.printlog("Connection failed after %s retries. Please check your internet connection. Exiting..." % retry['max'])
			sys.exit(1)
	
		return page

	def savepage(self, url, fn):
		page = self.readpage(url)
		save = self.file(fn)
		save.Write(page)

	def unescape(self, str): # unescape html symbols
		str = str.decode('utf-8')
		str = HTMLParser().unescape(str)
		return str