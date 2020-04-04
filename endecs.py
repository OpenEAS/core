from endec.softwareendec import SoftwareEndec

software = SoftwareEndec("ENDEC-S-1", "http://localhost:5000", cap_server="https://alerts.weather.gov/cap/us.php?x=0")

while True:
    software.monitor()
