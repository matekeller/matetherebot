#!/usr/bin/python3

import os
import requests
import json
from dotenv import find_dotenv, load_dotenv
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv((find_dotenv()))

aps = [
    "ap-2356-6u07",
    "ap-2356-6u09",
    "ap-2356-6u10b",
    "ap-2356-6u11",
    "ap-2356-5057",
    "ap-2356-5052",
    "ap-2356-6006",
    "ap-2356-6009",
    "ap-2356-6011",
    "ap-2356-6013",
    "ap-2356-6001a"
]

headers = {"Accept": "application/json"}

response = requests.request(
    method="GET",
    url="https://findme.rwth-aachen.de/client-info.json",
    headers=headers,
    verify=False,
).json()

if response.get("html"):
    soup = BeautifulSoup(response.get("html"), "html.parser")

    ap = soup.find("th", string="Access Point").find_next_sibling("td").string

    if ap in aps:
        requests.post(
            os.environ.get("URL") + "/max_present",
            json={"max_token": os.environ.get("MAXTHERE_TOKEN")},
        )
