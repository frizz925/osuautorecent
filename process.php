<?php
require_once('file.php');
require_once('config.php');

function ProcessRequest() {
	# get userid out of POST request
	$userid = $_POST["userid"];

	# do sanity checks on the userid
	if (empty($userid)) {
		return "Error: No user ID was entered!<br>";
	} else if (!is_numeric($userid)) {
		return "Error: User ID must be numeric!<br>";
	}

	$ids = array();
	foreach (file(TOKENS) as $line) {
		$line = trim($line);
		$parts = explode(" ", $line);
		array_push($ids, $parts[0]);
	}

	# check if userid already exists
	if (in_array($userid, $ids)) {
		return "Error: That user ID already exists in the database!<br>";
	}

	# save userid in the session
	session_start();
	$_SESSION['userid'] = $userid;

	# start processing request
	header('Location: ./redirect.php'); 
}

$content = ProcessRequest();
include('response.inc');
?>