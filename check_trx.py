import time
import requests
import json
import pytz
from datetime import datetime
import urllib.parse

last_timestamp = (int(time.time()) - 10) * 1000
current_timestamp = int(time.time()) * 1000

def check():

    url = (
        "https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=200&start=0&address=TXxqYjF2mjyDdHEmiadXiEiudkbL7nFmUZ"
        f"&start_timestamp={last_timestamp}&end_timestamp={current_timestamp}"
    )

    print(url)

    re = requests.get(url=url)
    print(re.text)

    reJson = json.loads(re.text)

    if len(reJson["data"]) > 0:
        for data in reJson["data"]:
            if data["toAddress"] == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t": #USDT address
                hash = data["hash"]
                check_url = urllib.parse.quote(f"https://tronscan.org/#/transaction/{hash}")
                confirmed = data["confirmed"]
                timestamp = int(data["timestamp"] / 1000)
                date = datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Phnom_Penh'))
                amount = int(data["trigger_info"]["parameter"]["_value"]) / (10 ** 6)

                tg_url = (
                    "https://api.telegram.org/bot5659808871:AAECEr2xHQqT8eKpqwnV5OS7L7bULhYfJao/sendMessage?chat_id=363937750&parse_mode=markdown&text="
                    ">>>>>>>>>>New Deposit<<<<<<<<<<\n"
                    f"Date: {date}\n"
                    f"Confirmed: {confirmed}\n"
                    f"Amount: {amount}USDT\n\n"
                    f"[Click to Open]({check_url})"
                )

                requests.get(url=tg_url)

# check()
while True:
    check()
    time.sleep(3)
    last_timestamp = current_timestamp
    current_timestamp = int(time.time()) * 1000
