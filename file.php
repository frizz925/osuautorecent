<?php
function FileWrite($fn, $str) {
	$f = fopen($fn, 'w');
	fwrite($f, $str);
	fclose($f);
}

function FileAppend($fn, $str) {
	$f = fopen($fn, 'a');
	fwrite($f, $str);
	fclose($f);
}

function FileCheck($fn, $str="") {
	if (!file_exists($fn)) { FileWrite($fn, $str); }
}
?>