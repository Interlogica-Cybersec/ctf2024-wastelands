<?php

$id = isset($_GET['id']) ? intval($_GET['id']) : 0;
header('Content-Type: application/json; charset=utf-8');
$success =  isset($_COOKIE["SUCCESS_COOKIE"]) && $_COOKIE["SUCCESS_COOKIE"] == getenv('SUCCESS_COOKIE');

if ($id == 1) {
    if ($success) {
        $title = "System main configuration";
        $message = "System configuration:";
        $config = "# Hydroponics Lab Configuration File
lab_name: Ark Hydroponics Lab
system_type: Nutrient Film Technique (NFT)
lighting:
  type: LED
  spectrum: Full Spectrum
  schedule: 18 hours on, 6 hours off
nutrient_solution:
  pH: 5.8
  ec: 1.5 mS/cm
  temperature: 18°C
  reservoir_capacity: 200 liters
air_control:
  temperature: 24°C
  humidity: 55%
  co2_enrichment: Yes
  ventilation: Active, with carbon filters
monitoring_system:
  software_version: 3.2.1
  sensors:
    - pH
    - EC
    - Temperature
    - Humidity
    - CO2 Levels
  alerts:
    - Nutrient Solution Low
    - pH Imbalance
    - High Temperature
    - Low Humidity
    - CO2 Levels Abnormal
backup_systems:
  power: Spintronic battery, 3kWh
  nutrient_solution: Manual mixing available
  air_control: Manual override available";
        $no_slashr = str_replace("\r", "", $config);
        $no_newlines = str_replace("\n", "<br>", $no_slashr);
        $content =  str_replace(" ", "&nbsp;", $no_newlines);
    } else {
        $title = "System main configuration error";
        $message = "Could not parse main system configuration. <br> Current configuration file content:";
        $content = "Get rekt b*tches. Enjoy my useless bunker<br>~ Mark";
    }
} else if ($id == 2) {
    $title = "FTP subsystem configuration";
    $message = "FTP subsystem configuration file content:";
    $no_slashr = str_replace("\r", "", file_get_contents('/etc/vsftpd.conf'));
    $content = str_replace("\n", "<br>", $no_slashr);
} else {
    $title = "Service ID not recognized";
    $message = "System service ID not recognized. Valid ids are: [1, 2]";
    $content = "";
}
?>
{
"title": "<?php echo $title ?>",
"message": "<?php echo $message ?>",
"content": "<?php echo $content ?>"
}
