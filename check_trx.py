import time
import requests
import json
import pytz
import urllib.parse
import random
import subprocess
from PIL import Image
from datetime import datetime
from requests import HTTPError

last_timestamp = (int(time.time()) - 3) * 1000
current_timestamp = int(time.time()) * 1000

def check():

    url = (
        "https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=100&start=0&address=TXxqYjF2mjyDdHEmiadXiEiudkbL7nFmUZ"
        f"&start_timestamp={last_timestamp}&end_timestamp={current_timestamp}"
    )

    print(url)

    re = requests.get(url=url)
    print(re.text)

    reJson = json.loads(re.text)

    if len(reJson["data"]) > 0:
        for data in reJson["data"]:
            if data["toAddress"] == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" and data["ownerAddress"] != "TXxqYjF2mjyDdHEmiadXiEiudkbL7nFmUZ": #USDT address
                hash = data["hash"]
                check_url = urllib.parse.quote(f"https://tronscan.org/#/transaction/{hash}")
                confirmed = data["confirmed"]
                timestamp = int(data["timestamp"] / 1000)
                date = datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Phnom_Penh'))
                amount = int(data["trigger_info"]["parameter"]["_value"]) / (10 ** 6)
                wait = random.randint(3, 15)

                tg_url = (
                    "https://api.telegram.org/bot5659808871:AAECEr2xHQqT8eKpqwnV5OS7L7bULhYfJao/sendMessage?chat_id=363937750&parse_mode=markdown&text="
                    ">>>>>>>>>>New Deposit<<<<<<<<<<\n"
                    f"Date: {date}\n"
                    f"Confirmed: {confirmed}\n"
                    f"Amount: {amount}USDT\n"
                    f"Screenshot wait: {wait} second\n\n"
                    f"[Click to Open]({check_url})"
                )

                requests.get(url=tg_url)
                take_screenshot(hash=hash, wait=wait)


def take_screenshot(hash: str, wait: int):
    print(f"Waiting Screenshot {wait} second")
    wait *= 1000
    subprocess.run(["shot-scraper", f"https://tronscan.org/#/transaction/{hash}", "-o", "photo.jpg", "--wait", f"{wait}"
    # , "--width", "1424", "--height", "750"
    ])
    crop_photo()
    send_photo()

# pip install shot-scraper
# # Now install the browser it needs:
# shot-scraper install

def crop_photo():
    img = Image.open(r"photo.jpg") 
 
    left = random.randint(0, 150)
    top = random.randint(50, 150)
    right = random.randint(1294, 1424)
    bottom = random.randint(650, 750)
    
    img_res = img.crop((left, top, right, bottom)) 
    img_res = img_res.convert('RGB')
    img_res.save("photo.jpg")

def send_photo(image_caption=""):
    data = {"chat_id": "363937750", "caption": image_caption}
    url = "https://api.telegram.org/bot5659808871:AAECEr2xHQqT8eKpqwnV5OS7L7bULhYfJao/sendDocument"
    with open("photo.jpg", "rb") as image_file:
        requests.post(url, data=data, files={"document": image_file})

# check()
while True:
    try:
        check()
    except HTTPError as ex:
        print(f"Error: {ex}")
    time.sleep(3)
    last_timestamp = current_timestamp
    current_timestamp = int(time.time()) * 1000
