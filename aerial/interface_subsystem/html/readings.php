<?php
header('Content-Type: application/json');

$host = 'data_subsystem';
$dbname = 'sensors';
$username = 'kestrel';
$password = '856a0e059c03';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $stmt = $pdo->prepare("SELECT * FROM sensor_readings");
    $stmt->execute();
    $readings = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode(['status' => 'success', 'readings' => $readings]);
} catch (PDOException $e) {
    echo json_encode(['status' => 'error', 'message' => 'Data subsystem is offline']);
}
?>
