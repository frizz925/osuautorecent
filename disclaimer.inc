<form method="post">
	<h2>Disclaimer</h2>
	This application is currently <b>closed source</b> due to its instability. It will be available as <b>open source</b> in the future as soon as it becomes stable.<br>
	<br>
	This is still an <b>experimental</b> work in progress, which means it's still <b>highly unstable</b> yet usable. Should you revoke any and all access by this application and report it right away in case of something went wrong.<br>
	During the registration process, you are required to authorize this application to your Twitter account and your access tokens will be stored in the database. These tokens will <b>never</b> be misused.<br>
	In a scenario where these tokens get compromised, you <b>must</b> revoke this application access right away to keep your Twitter account safe.<br>
	<br>
	By agreeing to these terms, you will also agree to opt-in to testing this application and <b>to use it by your own risk</b>. You are also helping out this project by testing it.<br>
	I will not take responsibility for any damage done by this application. Again, this is still <b>highly unstable</b>.<br>
	<br>
	A total of <?php echo $usercount ?> different users have used this application.<br>
	<span style="font-size: 12px;">Sshh... need to remove your tokens? <a href="./remove">Go here!</a></font><br>
	<input type="submit" value="I agree">
	<input type="hidden" name="agreement" value="1">
</form>