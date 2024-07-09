<?php
header('Content-Type: application/json');
libxml_disable_entity_loader(false);

function verify_activation_code($data) {

    if (!isset($data['code'])) {
        echo json_encode(['success' => false, 'message' => 'Code not provided']);
        exit();
    }
    if (empty(trim($data['code']))) {
        echo json_encode(['success' => false, 'message' => 'Code not provided']);
        exit();
    }
    $params = [
        'activation_code' => trim($data['code'])
    ];
    $query_params = http_build_query($params);
    $url = 'http://security_subsystem/activate.php?' . $query_params;
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, false);
    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        echo json_encode(['success' => false, 'message' => curl_error($ch), 'code' => $data['code']]);
        exit();
    } else {
        $httpStatusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpStatusCode == 200) {
            echo json_encode(['success' => true, 'message' => $response]);
        } else {
            echo json_encode(['success' => false, 'message' => $response, 'code' => $data['code']]);
        }
        exit();
    }
}
$rawData = file_get_contents('php://input');
$contentType = $_SERVER['CONTENT_TYPE'];
$data = null;
if (strpos($contentType, 'application/json') !== false) {
    $data = json_decode($rawData, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        echo json_encode(['success' => false, 'message' => 'Invalid JSON', 'input' => json_decode(json_encode($rawData), true)]);
        exit();
    }
    verify_activation_code($data);
    exit();
} elseif (strpos($contentType, 'application/xml') !== false || strpos($contentType, 'text/xml') !== false) {
    $xml = simplexml_load_string($rawData, 'SimpleXMLElement', LIBXML_NOENT | LIBXML_DTDLOAD);
    if ($xml === false) {
        echo json_encode(['success' => false, 'message' => 'Invalid XML', 'input' => json_decode(json_encode($rawData), true)]);
        exit();
    }
    $data = json_decode(json_encode($xml), true);
    verify_activation_code($data);
    exit();
} else {
    echo json_encode(['success' => false, 'message' => 'Unsupported Content-Type']);
    exit();
}
?>
