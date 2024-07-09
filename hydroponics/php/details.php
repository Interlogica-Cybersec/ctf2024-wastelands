<?php
$plantId = isset($_GET['id']) ? intval($_GET['id']) : 0;
if ($plantId == 7) { // adv glitch
    header('Location: /dfsec.php');
    exit;
}

$filePath = 'details/' . $plantId;
if (file_exists($filePath)) {
    echo file_get_contents($filePath);
} else {
?>
<div>UNEXPECTED ERROR!!</div>
<!-- TODO: customize this error message -->
<!-- TODO: also fix that problem with the proxy once I figure how to do it -->
<?php
}
 ?>