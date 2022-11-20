import subprocess
import os
import requests
import json
from dotenv import find_dotenv, load_dotenv

load_dotenv((find_dotenv()))

aps = [
    "04:5F:B9:2F:56:2F",
    "54:8A:BA:CC:80:AF",
    "04:5F:B9:2F:7D:AF",
    "04:5F:B9:2F:89:6F",
    "54:8A:BA:CD:83:CF",
    "54:8A:BA:CD:83:C0",
    "14:16:9D:56:B4:C0",
    "04:5F:B9:2F:78:8F",
    "54:8A:BA:CB:AE:4F",
    "54:8A:BA:CD:76:6F",
    "54:8A:BA:CB:AC:AF",
    "54:8A:BA:CD:67:4F",
    "14:16:9D:55:92:60"
]

iwconfig = subprocess.Popen(('iwconfig', 'wlp0s20f3'), stdout=subprocess.PIPE)

output = subprocess.check_output(
    ('grep', '-P', "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", '-o'), stdin=iwconfig.stdout).strip()
iwconfig.wait()
output = output.decode('ascii')

if (output in aps):
    requests.post(os.environ.get('URL') + '/max_present', json={"max_token": os.environ.get('MAXTHERE_TOKEN')})
    print(output)
