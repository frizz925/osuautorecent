# osuautorecent
Part of my little Automation Project. This is basically a Twitter application for posting recent activities from osu! to user's Twitter account.

# Requirements
* Python 2 (2.7 recommended)
* PHP 5 (5.3 recommended)

# Libraries used
* JavaScript
	* [jQuery 2.0.3](https://jquery.com/)
* Python
	* [python-twitter](https://github.com/bear/python-twitter)
* PHP
	* [twitteroauth](https://github.com/abraham/twitteroauth)

# Changelog
* 08/07/2013
	* General
		* Whole new looks for the page, supported with jQuery.
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