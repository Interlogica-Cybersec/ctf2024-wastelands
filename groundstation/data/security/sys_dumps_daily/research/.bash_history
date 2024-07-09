gcc -o satellite_control satellite_control.c
./satellite_control
gcc -o telemetry_monitor telemetry_monitor.c
./telemetry_monitor
exit
gcc -o orbit_calculator orbit_calculator.c
./orbit_calculator
vim payload_analysis.c
gcc -o payload_analysis payload_analysis.c
./payload_analysis
mv payload_analysis bin
gcc -o antenna_alignment antenna_alignment.c
./antenna_alignment
vim data_processing.c
gcc -o data_processing data_processing.c
./data_processing
mv data_processing bin
gcc -o solar_panel_calibration solar_panel_calibration.c
./solar_panel_calibration
vim sensor_calibration.c
exit
gcc -o sensor_calibration sensor_calibration.c
./sensor_calibration
gcc -o communication_protocol communication_protocol.c
./communication_protocol
gcc -o navigation_system navigation_system.c
./navigation_system
mv *.c src
exit
