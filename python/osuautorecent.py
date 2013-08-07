#!/usr/bin/env python2.7

from funcslib import *
import os, sys, time
import urllib2

funcs = Functions(__file__)
json_dict = funcs.decodelocaljson()

cachedir = os.path.join(funcs.scriptdir, "cache")
if not os.path.exists(cachedir): # make cache directory if not exist
	os.makedirs(cachedir)

def eventfix(html, username): # function used to remove html tags and makes text much more proper for tweeting
	verbs = {
		"has"	: "have",
		"their"	: "my"
	}

	# remove tags
	html = funcs.strip_tags(html)
	
	# replace username
	html = html.replace(username, "I", 1)

	# fix verbs
	for v in verbs:
		html = html.replace(v, verbs[v])

	# remove whitespace
	html = html.strip()

	return html

def main():
	# switches
	useTestKeys = False
	dontTweet = False
	dontCache = False
	if len(sys.argv) > 1:
		if "testkeys" in sys.argv[1:]:
			funcs.printlog("Using test access tokens.")
			useTestKeys = True
		if "nocache" in sys.argv[1:]:
			funcs.printlog("No caching.")
			dontCache = True
		if "notweet" in sys.argv[1:]:
			funcs.printlog("No tweet posting.")
			dontTweet = True

	# load the on-site tokens file
	tokens = funcs.readpage(json_dict["tokens_url"])

	# save tokens for backup fgsfds
	save = funcs.file(os.path.join(funcs.scriptdir, json_dict["tokens_file"]))
	save.Write(tokens)

	# iterate tokens
	tokens = tokens.split("\n")

	# list of valid ids
	validids = []

	for line in tokens: # read the tokens file
		line = line.strip()

		# ignore whitespace
		if not line: continue

		# 0: userid/username, 1: access key, 2: access secret
		keys = line.split() 
		
		# grab userid
		userid = keys[0]

		# append userid to valid ids for user cache validation
		validids.append(userid)

		# use test access tokens
		if useTestKeys:
			keys[1] = json_dict["test_access_keys"][0]
			keys[2] = json_dict["test_access_keys"][1]

		# register Twitter API class
		twitter_keys = [json_dict["app_keys"][0], json_dict["app_keys"][1], keys[1], keys[2]]
		twitter = funcs.twitter(twitter_keys)

		# register file handling class for user cache
		cache = funcs.file(os.path.join(cachedir, userid + ".db"))

		# access osu!api
		# thanks to osu!api, everything's done much more easier now and it now accepts username
		page = funcs.readpage("http://osu.ppy.sh/api/get_user?k=%s&u=%s" % (json_dict["osuapi_key"], userid))

		# decode json from osu!api
		osu_api_json = json.loads(page)
		username = osu_api_json[0]["username"]
		events = osu_api_json[0]["events"]

		# user doesn't have any recent activity yet
		if not events: 
			cache.Write("") # just create an empty cache for now
			continue

		# handle data gathering, tweet posting, and caching
		for event in reversed(events):
			# handle data gathering
			activity = event["display_html"]
			activity = eventfix(activity, username)
			data = event["date"] + " " + activity

			# handle tweet posting and caching
			cached = cache.ReadToList()
			if cached and not cache.wasEmpty: # cache exists
				if not data in cached: # check if activity is new
					# no tweet mode
					if not dontTweet:
						twitter.PostTweet(activity, suffix=json_dict["tweet_suffix"]) # post tweet

					# no caching mode 
					if not dontCache:
						cache.AppendLine(data) # create a new cache and append all the activities
			else: # cache doesn't exist/empty
				cache.AppendLine(data) # create a new cache and append all the activities
				if not cache.wasEmpty:
					cache.wasEmpty = True

		if cache.wasEmpty:
			funcs.printlog("Created " + cache.fn)

	# user cache validation
	for fn in os.listdir(cachedir):
		 if not fn.replace(".db", "") in validids: # invalid cache removal - normally due to the user removing their tokens
			fn = os.path.join(cachedir, fn)
			funcs.printlog("Removed %s" % fn)
			os.remove(fn)

	funcs.printlog("Exited successfully.") # process done

	# check for pid. if not found or differs from the current one, exit process
	pidfile = funcs.file(os.path.join(funcs.scriptdir, funcs.pidfn))
	if not pidfile.CheckFile() or pidfile.ReadToString() != str(os.getpid()):
		sys.exit(0)

	# sleep and loop the process
	try:
		time.sleep(json_dict["timeout"])
	except:
		sys.exit(0)
	main()

if __name__ == '__main__':
	funcs.printpid()
	main()