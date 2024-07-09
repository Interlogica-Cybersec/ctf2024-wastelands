<?php
header('Content-Type: text/plain');

$host = 'data_subsystem';
$dbname = 'settings';
$username = 'security';
$password = 'e9838f5e68811ce3';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $stmt = $pdo->prepare("SELECT value FROM settings where name='activation_code'");
    $stmt->execute();
    $setting = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($setting and $setting['value'] != null) {
        if (!isset($_GET['activation_code']) || $_GET['activation_code'] !== $setting['value']) {
            header('HTTP/1.1 401 Unauthorized');
            echo 'Unauthorized';
        } else {
            $stmt = $pdo->prepare("UPDATE settings SET value = 'activated' where name='status'");
            $stmt->execute();
            echo "Drone activated";
        }
    } else {
        header('HTTP/1.1 525 Factory reset required');
        echo 'Factory reset required';
    }
} catch (PDOException $e) {
    header('HTTP/1.1 500 Internal server error');
    echo 'Could not connect to the database';
}
?>