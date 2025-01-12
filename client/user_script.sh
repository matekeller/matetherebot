#!/usr/bin/env sh

aps=("04:5F:B9:2F:56:2F"
    "54:8A:BA:CC:80:AF"
    "04:5F:B9:2F:7D:AF"
    "04:5F:B9:2F:89:6F"
    "54:8A:BA:CD:83:CF"
    "54:8A:BA:CD:83:C0"
    "14:16:9D:56:B4:C0"
    "04:5F:B9:2F:78:8F"
    "54:8A:BA:CB:AE:4F"
    "54:8A:BA:CD:76:6F"
    "54:8A:BA:CB:AC:AF"
    "54:8A:BA:CD:67:4F"
    "14:16:9D:55:92:60"
    "04:5F:B9:2F:78:80"
    "54:8A:BA:CD:76:60"
    "04:5F:B9:2F:7D:AD"
    "54:8A:BA:CC:80:A2"
    "54:8A:BA:CD:76:6D"
    "04:5F:B9:2E:D2:8D"
    "04:5F:B9:2F:78:8D"
    "04:5F:B9:2F:89:6D"
    "04:5F:B9:2F:78:82"
    "04:5F:B9:2F:56:22"
    "04:5F:B9:2F:56:2D"
    "54:8A:BA:CC:80:AD"
    "14:16:9D:55:7B:22"
    "54:8A:BA:CD:67:4D"
    "04:5F:B9:2F:56:2E"
    "54:8A:BA:CC:80:A1"
    "04:5F:B9:2F:56:21"
    "04:5F:B9:2F:7D:AE"
    "04:5F:B9:2F:78:81"
    "54:8A:BA:CD:67:4E"
    "04:5F:B9:2F:89:6E")

if [[ $(iwgetid -r) != "eduroam" ]]; then
    exit 0
fi

re="(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)"

if [[ $(iwgetid -a) =~ $re ]]; then
    ap=${BASH_REMATCH[1]}

    if [[ $(echo ${aps[@]} | grep -F -w $ap) ]]; then
        echo "Found AP which is in AP List: $ap"
        echo "Sending presence ping..."
    else
        echo "Connected to eduroam, but AP does not match. Exiting..."
        exit 0
    fi
fi

result=$(curl -X POST $URL/max_present -H "Content-Type: application/json" -d "{ \"max_token\": \"$MAXTHERE_TOKEN\" }")

echo $result