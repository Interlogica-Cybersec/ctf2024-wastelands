<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <title>The Kestrel - Reconnaissance Drone Control System</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
    .dfsec-img {
        width: 15rem;
        margin: auto;
    }
    </style>
</head>
<body>
<div class="wrapper">
<div class="title" onclick="location='/'">THE KESTREL</div>
<div class="subtitle" onclick="location='/'">Military reconnaissance Drone</div>
<div id="readingsContainer">
    <div class="section-title">Technical specifications:</div>
    <div>
        <div>Length: <span>45 cm</span></div>
        <div>Wing span: <span>65 cm</span></div>
        <div>Weight: <span>1.4 kg</span></div>
        <div>Model: <span>Fixed wing</span></div>
        <div>Propulsion: <span>Internal, Ionic</span></div>
        <div>Top speed: <span>120 km/h</span></div>
        <div>Max altitude: <span>9 km</span></div>
        <div>Cruise altitude: <span>5 km</span></div>
        <div>Round-trip range: <span>195 km</span></div>
        <div>Navigation modes: <span>Manual/Automatic/AI driven</span></div>
        <div>Coordinates retrieval: <span>GPS/Landscape waypoints</span></div>
        <div>Glitch provider: <span onclick="location='/gl33tch.php'" class="underlined">error</span></div>
        <div>Camera sensor: <span>CMOS, 130 MPX</span></div>
        <div>Camera aperture: <span>55 mm</span></div>
        <div>Camera zoom: <span>400x</span></div>
    </div>
</div>
<img id="kestrel" src="static/kestrel.png">
<div class="footer">ESAP - Technology through Defense, Defence through Technology</div>
</div>

<div id="modal" class="modal-bg">
    <div class="modal">
        <div class="modal-title">
            <div>Congratulations!</div>
        </div>
        <div class="horizontal-container modal-content">You found an ADV Glitch! Dataflow Security #3</div>
        <div class="horizontal-container modal-content"><img class="dfsec-img" src="/static/dfsec-logo-bw.svg"></div>
        <div class="horizontal-container modal-content">Dataflow Security - Mastering in vulnerability research - <a target="_blank" href="https://dfsec.com">dfsec.com</a></div>
        <div class="horizontal-container modal-content">DFSEC{a460cc89-458b-41c2-b0a2-de160f10b1c8}</div>
        <div class="horizontal-container modal-content">
        <button onclick="history.back()">Yeee!</button>
        </div>
    </div>
</div>
</body>
</html>