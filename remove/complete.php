<?php
require_once('config.php');
require_once('../file.php');
require_once('../twitter/twitteroauth.php');

function CompleteRequest() {
	session_start();

	# missing request tokens
	if (empty($_SESSION['oauth_token'])) {
		return "Whoops. Something went wrong: The request tokens are missing. Please try again.<br>";
	}

	# old request tokens
	if (isset($_GET['oauth_token']) && $_SESSION['oauth_token'] !== $_GET['oauth_token']) {
		session_destroy();
		$_SESSION['oauth_status'] = 'oldtoken';
		return "Whoops. Something went wrong: The request tokens are either old or mismatched. Please try again.<br>";
	}

	$connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $_SESSION['oauth_token'], $_SESSION['oauth_token_secret']);
	$access_token = $connection->getAccessToken($_REQUEST['oauth_verifier']);

	# remove unneeded request tokens
	unset($_SESSION['oauth_token']);
	unset($_SESSION['oauth_token_secret']);

	# access tokens unavailable
	if (empty($access_token) || empty($access_token['oauth_token']) || empty($access_token['oauth_token_secret'])) {
		session_destroy();
		return "Whoops. Something went wrong: Your access tokens are not found!<br>";
	}

	$tokens = array();
	$data = array();
	foreach (file('../tokens.scrt') as $line) {
		$line = trim($line);
		$parts = explode(" ", $line, 2);
		array_push($tokens, $parts[1]);
		array_push($data, $line);
	}

	# access tokens don't exist
	$oauth = $access_token['oauth_token']." ".$access_token['oauth_token_secret'];
	if (!in_array($oauth, $tokens)) {
		return "Error: Your access tokens don't exist in the database.<br>";
	}

	# rewrite tokens database
	FileWrite('../tokens.scrt', "");

	$tokens = "";
	foreach ($data as $line) {
		$parts = explode(" ", $line, 2);
		if ($oauth != $parts[1]) {
			FileAppend('../tokens.scrt', $line."\n");
		}
	}

	# user tokens have been sucessfully stored in the database
	return "Success: Your tokens have been removed from the database.<br>";
}
$content = CompleteRequest();
include('response.inc');
?>