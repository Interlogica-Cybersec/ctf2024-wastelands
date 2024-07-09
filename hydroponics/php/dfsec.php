<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hydroponics</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="stylesheet" href="static/style.css">
    <script src="static/particles.js"></script>
    <style>
    .modal-content {
        display: flex;
    }
    .dfsec-img {
        width: 15rem;
        margin: auto;
    }
    </style>
</head>
<body onload="onBodyLoad()">
    <a href="." class="header">
        <div class="title-block">
            <div class="title">
            Hydroponics Management System
            </div>
            <div class="subtitle">
            Ark Technologies
            </div>
        </div>
    </a>
    <div class="modal-wrapper">
        <div class="modal">
            <div class="modal-header">Congratulations!</div>
            <div class="modal-content">You found an ADV Glitch! Dataflow Security #6</div>
            <div class="modal-content"><img class="dfsec-img" src="/static/dfsec-logo-bw.svg"></div>
            <div class="modal-content"><span>Vulnerability research is your thing? We're defining the forefront of innovation - <a target="_blank" href="https://dfsec.com">dfsec.com</a></span></div>
            <div class="modal-content">DFSEC{ae984f39-3d1a-42aa-88e0-b50aad7010da}</div>
            <div class="modal-buttons">
                <button onclick="location='/plants.php'">Wohooooo!</button>
            </div>
        </div>
    </div>
    <canvas id="particles" width="1536" height="378" class="particles"></canvas>
    <script>

function onBodyLoad() {
    particles(opacity=100, numParticles=10, sizeMultiplier=5, width=1, connections=true, connectionDensity=15, noBounceH=false, noBounceV=false, speed=3, avoidMouse=false, hover=true)
}
    </script>
</body>
</html>