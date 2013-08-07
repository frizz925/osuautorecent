<?php
# this is used for processing user's request before redirecting the user to the application authorization page
session_name("osuautorecent");
session_start();
require_once('file.php');
require_once('config.php');

function ProcessRequest() {
	# get userid and its type out of POST request
	$userid = $_POST["userid"];
	$usertype = $_POST["usertype"];

	# do sanity checks on the userid
	if (empty($userid)) {
		return "Error: Nothing was entered!";
	}

	# user input user ID but it's not numeric
	if ($usertype == "userid" && !is_numeric($userid)) {
		return "Error: osu! user ID must be numeric!";
	}

	# username/userid existence check
	$json_url = "http://osu.ppy.sh/api/get_user?k=".OSUAPI_KEY."&u=".urlencode($userid);
	$json = file_get_contents($json_url);
	$json_output = json_decode($json);

	# unexisting username/userid would return nothing from osu!api
	if (empty($json_output)) {
		return "Error: User not found!";
	}

	# convert username to user ID
	if ($usertype == "username") {
		$userid = $json_output[0]->user_id;
	}

	# get the list of tokens
	$ids = array();
	foreach (file(TOKENS) as $line) {
		$line = trim($line);
		$parts = explode(" ", $line);
		array_push($ids, $parts[0]);
	}

	# check if userid already exists
	if (in_array($userid, $ids)) {
		return "Error: That user ID already exists in the database!";
	}

	# save userid in the session
	$_SESSION['userid'] = $userid;

	# start processing request
	header('Location: ./redirect.php'); 
}

$message = ProcessRequest();
$page = 'form.inc';
include('home.inc');
?>