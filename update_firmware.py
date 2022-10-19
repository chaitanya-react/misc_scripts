import requests
import os


# Set AP Mode on ESP32:  BT send "Y" on characteristic "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# wait for maybe 5s

# Connect to Wifi with SSID: "ReactHardwareCB"  / Pass: "IfTzeitelMarriesLazarwolf"

# Run update:
esp_path = r"/Users/chaitanya/Documents/tablet_stuff/firmware_ota/ESP32FW.ino.esp32.bin"
files = {'file': open(esp_path, 'rb')}
requests.post("http://192.168.1.1/update", files=files)

# http://192.168.1.1/updateflag0 resets/aborts update
# once complete, connect to BT again
# do failure handling
