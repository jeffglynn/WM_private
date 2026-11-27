<?php
// Usage: php resize-one.php <src> <dest.jpg>  (800px wide card)
[$_, $src, $dst] = $argv;
$im = imagecreatefromstring(file_get_contents($src));
$w = imagesx($im); $h = imagesy($im); $r = min(1, 800 / $w);
$nw = (int) round($w * $r); $nh = (int) round($h * $r);
$o = imagecreatetruecolor($nw, $nh);
imagecopyresampled($o, $im, 0, 0, 0, 0, $nw, $nh, $w, $h);
imagejpeg($o, $dst, 82);
echo "$nw x $nh\n";
