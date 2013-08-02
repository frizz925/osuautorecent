<form action="process.php" method="post">
	<select id="usertype" name="usertype">
		<option value="userid">osu! user ID</option>
		<option value="username">osu! username</option>
	</select>
	<input type="text" name="userid" size="12"><input type="submit"><br>
	<span id="username_warn" style="display: none;">Your username will be converted into osu! user ID.<br></span>
	If everything goes correctly, you should be redirected to Twitter application authorization page.<br>
</form>
<script>
	var select = document.getElementById("usertype")
	var span = document.getElementById("username_warn")

	select.onchange = function () {
		if (select.options[select.selectedIndex].value == "userid") {
			span.style.display = "none"
		} else {
			span.style.display = "inline"
		}
	}
</script>