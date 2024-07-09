<?php
header('Glitch1: Congratulations!');
header('Glitch2: You found an ADV Glitch! DV Cyber Security #3');
header('Glitch3: Secure your IT infrastructure with comprehensive assessments and advanced protections for network, systems, and cloud.');
header('Glitch4: Find out more on https://dvcybersecurity.it');
header('Glitch5: DVCYBERSECURITY{c11f4390-c6b0-4836-9e69-89a130ba1b02}');
?>
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
<div class="title">THE KESTREL</div>
<div class="subtitle">Military reconnaissance Drone</div>
<div id="readingsContainer">
    <div class="section-title">Sensors readings:</div>
    <div id="readingsList">
        <div>Altimeter: <span id="altimeter"></span></div>
        <div>Roll: <span id="roll"></span></div>
        <div>Pitch: <span id="pitch"></span></div>
        <div>Yaw: <span id="yaw"></span></div>
        <div>Speed: <span id="speed"></span></div>
        <div>Battery level: <span id="battery_level"></span></div>
        <div>GPS coordinates: <span id="gps_coordinates"></span></div>
    </div>
</div>
<div id="statusContainer">
    <div class="section-title">Status:</div>
    <div class="horizontal-container">
        <div id="statusValue">
        </div>
        <button id="activate" class="hidden" onclick="onActivate()">Activate</button>
    </div>
</div>
<div id="techSpecsContainer">
    <div class="section-title">Tech specs:</div>
    <div class="horizontal-container">
        <button id="specs" onclick="onTechSpecs()">Show</button>
    </div>
</div>
<div id="controlsContainer">
    <div class="section-title">Controls:</div>
    <button id="controls" disabled='disabled' onclick="onControls()">Open controls</button>
</div>
<img id="kestrel" src="static/kestrel.png">
<div class="footer">ESAP - Technology through Defense, Defence through Technology</div>
</div>
<div id="modal" class="modal-bg hidden">
    <div class="modal">
        <div class="modal-title">
        <div>Activation code required</div>
        <svg class="close" onclick="onCloseModal()" viewbox="0 0 30 30">
            <line stroke="currentColor" stroke-linecap="round" stroke-width=5 x1="5" x2="25" y1="5" y2="25"></line>
            <line stroke="currentColor" stroke-linecap="round" stroke-width=5 x1="25" x2="5" y1="5" y2="25"></line>
        </svg>
        </div>
        <div class="horizontal-container modal-content">
            <input type="text" id="code" placeholder="Activation code">
            <button onclick="submitActivationCode()">Submit</button>
        </div>
        <div id="activationMessage" class="hidden"></div>
    </div>
</div>
<script>

    function fetchData() {
        fetchReadings();
        fetchStatus();
    }

    function fetchReadings() {
        var url = 'readings.php';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                displayReadings(response);
            }
        };
        xhr.onerror = function () {
            displayReadingError('Error fetching readings from the server.');
        };
        xhr.send();
    }

    function submitActivationCode() {
        var url = 'activate.php';
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            code.value = ''
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    displayActivationCodeMessage(response.message);
                    fetchStatus();
                } else {
                    displayActivationCodeError(response.message);
                }
            }
        };
        var formData = JSON.stringify({code: code.value});
        xhr.onerror = function () {
            displayActivationCodeError('Error fetching readings from the server.');
        };
        xhr.send(formData);
    }

    function displayActivationCodeMessage(message) {
        activationMessage.classList.remove('error')
        activationMessage.classList.remove('hidden')
        activationMessage.innerText = message
    }
    function displayActivationCodeError(message) {
        activationMessage.classList.add('error')
        activationMessage.classList.remove('hidden')
        activationMessage.innerText = message
    }

    function displayReadings(response) {
        if (response.status === 'success') {
            response.readings.forEach(function (reading) {
                const el = document.getElementById(reading.name)
                if (!el) {
                    return
                }
                el.innerText = reading.reading
            });
        } else {
            displayReadingError(response.message)
        }
    }

    function displayReadingError(message) {
        readingsList.innerText = message;
        readingsList.classList.add('error');
    }

    function fetchStatus() {
        var url = 'status.php';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                displayStatus(response);
            }
        };
        xhr.onerror = function () {
            displayReadingError('Error fetching status from the server.');
        };
        xhr.send();
    }

    function displayStatus(response) {
        if (response.status) {
            statusValue.innerText = response.description
            const inactive = response.status != 'active'
            if (inactive) {
                activate.classList.remove('hidden')
            } else {
                activate.classList.add('hidden')
            }
            controls.disabled = inactive
        } else {
            controls.disabled = true
            displayStatusError(response.message)
        }
    }

    function displayStatusError(message) {
        statusValue.innerText = message
        statusValue.classList.add('error')
    }

    function onActivate() {
        modal.classList.remove('hidden')
    }

    function onControls() {
        location='controls.php'
    }

    function onTechSpecs() {
        location='tech-specs.php'
    }

    function onCloseModal() {
        modal.classList.add('hidden')
        code.value = ''
        activationMessage.classList.add('hidden')
        activationMessage.classList.remove('error')
        activationMessage.innerText = ''
    }

    window.onload = fetchData;
</script>
</body>
</html>
