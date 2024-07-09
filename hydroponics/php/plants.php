<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hydroponics</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="stylesheet" href="static/style.css">
    <script src="static/particles.js"></script>
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
    <div class="wrapper">
        <div>
            <div class="section">
                <div class="section-title">
                    Plants list:
                </div>
                <div class="cards">
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Golden Glow Bell Peppers</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam te deserturus sum.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant1.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(1)">view details</button>
                    </div>
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Cascading Carrot Canopy</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam te deficiam.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant2.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(2)">view details</button>
                    </div>
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Crimson Cascade Tomatoes</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam circumferam et desererem te.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant3.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(3)">view details</button>
                    </div>
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Luminous Lavender Lettuce</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam te flere faciam.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant4.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(4)">view details</button>
                    </div>
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Enchanted Emerald Spinach</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam vale dicam.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant5.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(5)">view details</button>
                    </div>
                    <div class="card">
                        <div class="card-section-title">Common name:</div>
                        <div>Verdant Velvet Broccoli</div>
                        <div class="card-section-title">Latin name:</div>
                        <div>Numquam mendacium dicam et te laedam.</div>
                        <div class="image-wrapper">
                            <img class="plant-image" src="static/plant6.png">
                        </div>
                        <button class="details-button" onclick="viewDetails(6)">view details</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="modal-wrapper hidden" id="plantDetails">
        <div class="modal">
            <div class="modal-header">Plant details</div>
            <div class="modal-content" id="plantDetailsText"></div>
            <div class="modal-buttons">
                <button onclick="closeModal(plantDetails)">Close</button>
            </div>
        </div>
    </div>
    <canvas id="particles" width="1536" height="378" class="particles"></canvas>
    <script>
function openModal(modalWrapper) {
    modalWrapper.classList.remove('hidden')
}

function closeModal(modalWrapper) {
    modalWrapper.classList.add('hidden')
}
    
function onBodyLoad() {
    particles(opacity=100, numParticles=10, sizeMultiplier=5, width=1, connections=true, connectionDensity=15, noBounceH=false, noBounceV=false, speed=3, avoidMouse=false, hover=true)
}

function viewDetails(id) {
    fetch(`details.php?id=${id}`)
    .then(resp => resp.text())
    .then(html => {
        plantDetailsText.innerHTML = html
        openModal(plantDetails)
    })
    .catch(error => console.log(error))
}
    </script>
</body>
</html>