osuautorecent
=============

Part of my little Automation Project. This is basically a Twitter application for posting recent activities from osu! to user's Twitter account.

Requirements:
* Python 2.x (2.7 recommended)
	* Modules
		* [python-twitter][https://github.com/bear/python-twitter]
* PHP 5+

Libraries used:
* Python
	* [python-twitter][https://github.com/bear/python-twitter]
* PHP
	* [twitteroauth][https://github.com/abraham/twitteroauth]

To-do list:
* Encrypting tokens database for better security of user's tokens.

Changelog:
* 08/02/2013
	* General
		* Rewrote half of the code. Now utilizes osu!api rather than stripping off user's osu! profile page.
	* PHP
		* Tokens storing now allows registers using username rather than user ID thanks to osu!api.
	* Python
		* Added various switches for testing purposes such as "notweet", "nocache", and "testkeys".
		* Locally store tokens database (for backup purpose).