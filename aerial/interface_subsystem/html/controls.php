<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <title>The Kestrel - Reconnaissance Drone Control System</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<div class="wrapper">
<div class="title" onclick="location='/'">THE KESTREL</div>
<div class="subtitle" onclick="location='/'">Military reconnaissance Drone</div>
<img id="kestrel" src="static/kestrel.png">
<div class="footer">ESAP - Technology through Defense, Defence through Technology</div>
</div>

<?php
    $url = 'http://security_subsystem/controls.php';
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, false);
    $response = curl_exec($ch);
    $controls = json_decode($response, true);
?>
<div id="modal" class="modal-bg">
    <div class="modal">
        <div class="modal-title">
            <div>
<?php
if ($controls['enabled']) {
    echo 'Controls';
} else {
    echo 'Warning';
}
?>
             </div>
        </div>
        <div class="horizontal-container modal-content">
<?php
    echo $controls['content'];
?>
        </div>
        <div id="activationMessage" class="hidden"></div>
    </div>
</div>
</body>
</html>
