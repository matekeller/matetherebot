import os
import re
import subprocess

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv((find_dotenv()))

# Can be obtained via:
# `sudo iw dev wlp5s0 scan | jc --iw-scan | jq '.[] | select(.ssid == "eduroam") | .bssid'`
aps = {
    "04:5f:b9:2f:56:2f",
    "54:8a:ba:cc:80:af",
    "04:5f:b9:2f:7d:af",
    "04:5f:b9:2f:89:6f",
    "54:8a:ba:cd:83:cf",
    "54:8a:ba:cd:83:c0",
    "14:16:9d:56:b4:c0",
    "04:5f:b9:2f:78:8f",
    "54:8a:ba:cb:ae:4f",
    "54:8a:ba:cd:76:6f",
    "54:8a:ba:cb:ac:af",
    "54:8a:ba:cd:67:4f",
    "14:16:9d:55:92:60",
    "04:5f:b9:2f:78:80",
    "54:8a:ba:cd:76:60",
    "04:5f:b9:2f:7d:ad",
    "54:8a:ba:cc:80:a2",
    "54:8a:ba:cd:76:6d",
    "04:5f:b9:2e:d2:8d",
    "04:5f:b9:2f:78:8d",
    "04:5f:b9:2f:89:6d",
    "04:5f:b9:2f:78:82",
    "04:5f:b9:2f:56:22",
    "04:5f:b9:2f:56:2d",
    "54:8a:ba:cc:80:ad",
    "14:16:9d:55:7b:22",
    "54:8a:ba:cd:67:4d",
    "04:5f:b9:2f:56:2e",
    "54:8a:ba:cc:80:a1",
    "04:5f:b9:2f:56:21",
    "04:5f:b9:2f:7d:ae",
    "04:5f:b9:2f:78:81",
    "54:8a:ba:cd:67:4e",
    "04:5f:b9:2f:89:6e"
}
iw_devices = subprocess.run(["iw", "dev"], check=True, capture_output=True, text=True)
device_match = re.search(r"Interface (?P<device_name>\w+)", iw_devices.stdout)

iw_link = subprocess.run(
    ["iw", "dev", device_match["device_name"], "link"],
    check=True,
    capture_output=True,
    text=True,
)
bssid_match = re.search(r"Connected to (?P<bssid>[\w:]+)", iw_link.stdout)

if bssid_match["bssid"] in aps:
    print(bssid_match["bssid"])
    request = requests.post(
        os.environ["URL"] + "/max_present",
        json={"max_token": os.environ["MAXTHERE_TOKEN"]},
    )
    print("Resp:", request.status_code, request.reason)
