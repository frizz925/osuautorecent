<?php
session_name("osuautorecent");
session_start();
require_once('file.php');
require_once('config.php');
require_once('../twitter/twitteroauth.php');

function CompleteRequest() {

	# missing request tokens
	if (empty($_SESSION['oauth_token'])) {
		return "Whoops. Something went wrong: The request tokens are missing. Please try again.";
	}

	# old request tokens
	if (isset($_GET['oauth_token']) && $_SESSION['oauth_token'] !== $_GET['oauth_token']) {
		session_destroy();
		$_SESSION['oauth_status'] = 'oldtoken';
		return "Whoops. Something went wrong: The request tokens are either old or mismatched. Please try again.";
	}

	$connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $_SESSION['oauth_token'], $_SESSION['oauth_token_secret']);
	$access_token = $connection->getAccessToken($_REQUEST['oauth_verifier']);

	# remove unneeded request tokens
	unset($_SESSION['oauth_token']);
	unset($_SESSION['oauth_token_secret']);

	# access tokens unavailable
	if (empty($access_token) || empty($access_token['oauth_token']) || empty($access_token['oauth_token_secret'])) {
		return "Whoops. Something went wrong: Your access tokens are not found!";
	}

	# unset tokens
	session_destroy();

	$tokens = array();
	foreach (file(TOKENS) as $line) {
		$line = trim($line);
		$parts = explode(" ", $line, 2);
		array_push($tokens, $parts[1]);
	}

	# access tokens already exist
	if (in_array($access_token['oauth_token']." ".$access_token['oauth_token_secret'], $tokens)) {
		return "Error: Your access tokens already exist in the database!";
	}

	# append tokens to the database
	$userid = $_SESSION['userid'];
	FileAppend(TOKENS, $userid." ".$access_token['oauth_token']." ".$access_token['oauth_token_secret']."\n");

	# user tokens have been sucessfully stored in the database
	return "Success: Your tokens have been stored in the database!<br>
	Please note that the application <b>periodically</b> checks for a new recent activity every 5 minutes (it doesn't update realtime).";
}
$content = CompleteRequest();
include('response.inc');
?>