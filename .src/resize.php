<?php
// Resize source photos into web/images. Carousel: 640px tall (2x). Cards: 800px wide.
$root = '/var/www/html';
$jobs = ['summer' => ['h', 640], 'winter' => ['h', 640], 'cards' => ['w', 800]];
foreach ($jobs as $set => [$axis, $size]) {
  foreach (glob("$root/.src/$set/*") as $src) {
    $im = @imagecreatefromstring(file_get_contents($src));
    if (!$im) { echo "fail $src\n"; continue; }
    [$w, $h] = [imagesx($im), imagesy($im)];
    $r = $axis === 'h' ? $size / $h : $size / $w;
    if ($r > 1) $r = 1;
    $nw = (int) round($w * $r); $nh = (int) round($h * $r);
    $out = imagecreatetruecolor($nw, $nh);
    imagecopyresampled($out, $im, 0, 0, 0, 0, $nw, $nh, $w, $h);
    $name = preg_replace('/(-png)?\.\w+$/', '', basename($src)) . '.jpg';
    imagejpeg($out, "$root/web/images/$set/$name", 82);
    echo "$set/$name {$nw}x{$nh}\n";
  }
}
