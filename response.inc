<html>
	<head>
		<title>Automation Project</title>
		<link href="main.css" rel="stylesheet" type="text/css">
		<script>
			window.onload = setTimeout(function() { window.location = "./index.php" }, 3000)
		</script>
	</head>
	<body>
		<div class="wrapper">
			<h1>osu! Automated Recent Activity Tweet</h1>
			<?php print_r($content); ?>
			You will be redirected to the homepage in 3 seconds.
		</div>
	</body>
</html>