<?php
require_once('config.php');

function ShowPage() {
	$usercount = count(file(TOKENS));
	
	if (!empty($_POST["agreement"]) and $_POST["agreement"] == "1") {
		include('form.inc');
	} else {
		include('disclaimer.inc');
	}
}
?>

<html>
	<head>
		<title>Automation Project</title>
		<link href="main.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<div class="wrapper">
			<h1>osu! Automated Recent Activity Tweet</h1>
			<?php ShowPage() ?>
		</div>
	</body>
</html>