<h1>Shared Files</h1>
<?php
$targetFolder = 'uploads/';
$files = scandir($targetFolder);
foreach ($files as $file) {
    if ($file != '.' && $file != '..') {
        echo "<a href='$targetFolder$file'>$file</a><br>";
    }
}
?>
