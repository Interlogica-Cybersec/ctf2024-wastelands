<?php
if (isset($_POST['configurationFile'])) {
    $configurationFile = $_POST['configurationFile'];
    $env_passcode = getenv('PASSCODE');

    if ($env_passcode !== false && $configurationFile === $env_passcode) {
        setcookie('SUCCESS_COOKIE', getenv('SUCCESS_COOKIE'));
        echo "Configuration reset successful. ";
        echo getenv('FLAG');
    } else {
        echo "Invalid configuration file.";
    }
} else {
    echo "Configuration file not set.";
}
?>