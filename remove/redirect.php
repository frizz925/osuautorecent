<?php
session_start();
require_once('config.php');
require_once('../twitter/twitteroauth.php');

$connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET);
$request_token = $connection->getRequestToken(OAUTH_CALLBACK);

$_SESSION['oauth_token'] = $token = $request_token['oauth_token'];
$_SESSION['oauth_token_secret'] = $request_token['oauth_token_secret'];

switch ($connection->http_code) {
	case 200: # connection success
		$url = $connection->getAuthorizeURL($token);
		header('Location: ' . $url); # redirect to authorization page
		break;
	default: # connection fails
		$content = 'Could not connect to Twitter. Refresh the page or try again later.';
		include('../response.inc');
}
?>