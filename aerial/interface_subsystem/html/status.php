<?php
header('Content-Type: application/json');

$url = 'http://security_subsystem/status.php';
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, false);
$response = curl_exec($ch);

if (curl_errno($ch)) {
    echo json_encode(['status' => 'error', 'description' => 'error']);
} else {
    $httpStatusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($httpStatusCode == 200) {
        echo $response;
    } else {
        echo json_encode(['status' => 'error', 'description' => 'error']);
    }
}
?>
