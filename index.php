<?php
session_name("osuautorecent");
session_start();
require_once('config.php');
$message = "";

if (!empty($_POST["agreement"])) {
	$_SESSION["agreement"] = true;
}

if (!empty($_SESSION["agreement"])) {
	$page = 'form.inc';
} else {
	$page = 'disclaimer.inc';
}

include('home.inc');
?>