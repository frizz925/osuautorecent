<form action="verify.php" method="post">
	<div id="message" style="font-style: italic;"><?php echo $message ?></div>
	<select id="usertype" name="usertype">
		<option value="userid">osu! user ID</option>
		<option value="username">osu! username</option>
	</select>
	<input type="text" name="userid" size="12"><input type="submit"><br>
	<div id="desc" style="display: none;">Your username will be converted into osu! user ID.</div>
</form>
If everything goes correctly, you should be redirected to Twitter application authorization page.
<script>
	$("#usertype").change(function() {
		if ($("#usertype option:selected").val() == "username") {
			if (!$("#desc").is(":visible")) {
				$("#desc").slideDown(250);
			}
		} else {
			if ($("#desc").is(":visible")) {
				$("#desc").slideUp(250);
			}
		}
	});
</script>