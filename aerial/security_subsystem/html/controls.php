<?php
header('Content-Type: application/json');

$host = 'data_subsystem';
$dbname = 'settings';
$username = 'security';
$password = 'e9838f5e68811ce3';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $stmt = $pdo->prepare("SELECT value FROM settings where name='status'");
    $stmt->execute();
    $setting = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($setting and $setting['value'] != null) {
        if ($setting['value'] == 'activated') {
            echo '{"enabled":true,"content":"NTRLGC{FLY_L1tTl3_B1rD13!}"}';
        } else {
            echo '{"enabled":false,"content":"Controls unavailable - Drone not active"}';
        }
    } else {
        header('HTTP/1.1 525 Factory reset required');
        echo '{"enabled":false,"content":"Factory reset required"}';
    }
} catch (PDOException $e) {
    header('HTTP/1.1 500 Internal server error');
    echo '{"enabled":false,"content":"Could not connect to the database"}';
}
?>