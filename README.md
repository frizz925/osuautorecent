# osuautorecent
Part of my little Automation Project. This is basically a Twitter application for posting recent activities from osu! to user's Twitter account.

# Requirements
* Python 2.x (2.7 recommended)
	* [python-twitter](https://github.com/bear/python-twitter)
		* [SimpleJson](http://cheeseshop.python.org/pypi/simplejson)
		* [SimpleGeo's OAuth2](http://github.com/simplegeo/python-oauth2) or [OAuth2](http://pypi.python.org/pypi/oauth2)
		* [HTTPLib2](http://code.google.com/p/httplib2/)
* PHP 5.3+

# Libraries used
* Python
	* [python-twitter](https://github.com/bear/python-twitter)
* PHP
	* [twitteroauth](https://github.com/abraham/twitteroauth) (included)

# To-do list
* Encrypting tokens database on-the-fly for better security of user's tokens.

# Changelog
* 08/02/2013
	* General
		* Rewrote half of the code. Now utilizes osu!api rather than stripping off user's osu! profile page.
	* PHP
		* Tokens storing now allows registers using username rather than user ID thanks to osu!api.
	* Python
		* Added various switches for testing purposes such as "notweet", "nocache", and "testkeys".
		* Locally store tokens database (for backup purpose).
* 07/31/2013
	* First release