<?php $success = isset($_COOKIE["SUCCESS_COOKIE"]) && $_COOKIE["SUCCESS_COOKIE"] == getenv('SUCCESS_COOKIE') ?>
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
        <div class="container">
            <img class="main-image" src=static/plant.png>
            <div>
                <div class="section">
                    <div class="section-title">
                        Plant status:
                    </div>
                    <div class="section-value">
                        <?php if ($success) {
                            echo "Healthy";
                        } else {
                            echo "Critical, plants severely wilted";
                        }
                        ?>
                    </div>
                </div>
                <div class="section">
                    <div class="section-title">
                        System status:
                    </div>
                    <div class="section-value">
                        <?php if ($success) {
                            echo "Nominal";
                        } else {
                            echo "Automatic irrigation deactivated";
                        }
                        ?>
                    </div>
                </div>
                <?php if (!$success) { ?>
                <div class="section">
                    <div class="section-title">
                        Reason:
                    </div>
                    <div class="section-value">
                        System configuration parse error
                    </div>
                </div>
                <div class="section">
                    <div class="section-title">
                        Recommended action:
                    </div>
                    <div class="section-value">
                        Reset main system configuration
                    </div>
                </div>
                <?php } ?>
            </div>
        </div>
        <div class="section">
            <div class="section-title">
                Actions:
            </div>
            <div class="actions-wrapper">
                <button onclick="viewPlants()">View plants</button>
                <button onclick="getSystemConfiguration()">View system configuration</button>
                <button onclick="openResetSystemConfigurationModal()">Reset main system configuration</button>
            </div>
        </div>
    </div>

    <div class="modal-wrapper hidden" id="viewSystemConfigurationModal">
        <div class="modal">
            <div class="modal-header" id="systemConfigurationTitle"></div>
            <div class="modal-content" id="systemConfigurationMessage"></div>
            <div class="modal-code-block" id="systemConfigurationContent"></div>
            <div class="modal-buttons">
                <button onclick="closeModal(viewSystemConfigurationModal)">Close</button>
            </div>
        </div>
    </div>

    <div class="modal-wrapper hidden" id="resetSystemConfigurationModal">
        <div class="modal">
            <div class="modal-header">Reset system configuration</div>
            <div class="modal-content">
                Insert the configuration file you want to load:
                <form action="reset_configuration.php" method="POST" id="resetConfigurationForm" class="reset-form">
                    <label for="configurationFile">Configuration file</label>
                    <input type="configurationFile" id="configurationFile" name="configurationFile" placeholder="Configuration file name">
                </form>
                <div id="message" class="hidden message"></div>
            </div>
            <div class="modal-buttons">
                <button onclick="closeModal(resetSystemConfigurationModal)">Close</button>
                <button onclick="resetConfiguration()">Reset</button>
            </div>
        </div>
    </div>
    <canvas id="particles" width="1536" height="378" class="particles"></canvas>
    <script>
function viewPlants() {
    location='plants.php'
}

function openModal(modalWrapper) {
    modalWrapper.classList.remove('hidden')
}

function closeModal(modalWrapper) {
    modalWrapper.classList.add('hidden')
}

function openResetSystemConfigurationModal() {
    message.classList.add('hidden')
    configurationFile.value = ''
    openModal(resetSystemConfigurationModal)
}

function getSystemConfiguration() {
    fetch('system_configuration.php?id=1')
    .then(resp => resp.json())
    .then(value => {
        systemConfigurationTitle.innerHTML = value.title
        systemConfigurationMessage.innerHTML = value.message
        systemConfigurationContent.innerHTML = value.content
        openModal(viewSystemConfigurationModal)
    })
    .catch(error => console.log(error))
}

function onBodyLoad() {
    particles(opacity=100, numParticles=10, sizeMultiplier=5, width=1, connections=true, connectionDensity=15, noBounceH=false, noBounceV=false, speed=3, avoidMouse=false, hover=true)
}

function resetConfiguration() {
    const formData = new FormData(resetConfigurationForm);
    message.classList.remove('hidden')
    message.innerText = 'Resetting system configuration...'
    fetch('reset_configuration.php', {
        method: 'POST',
        body: formData
    })
    .then(async response => {
        return {data: await response.text(), status: response.status};
    })
    .then(({data, status}) => {

        message.innerText = data || ''
    })
    .catch(error => {
        message.innerText = error || ''
    });
}

resetConfigurationForm.addEventListener('submit', function(event) {
    event.preventDefault();
    resetConfiguration()
});
    </script>
</body>
</html>