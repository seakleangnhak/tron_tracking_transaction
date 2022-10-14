import subprocess

subprocess.run(["shot-scraper", "https://tronscan.org/#/transaction/6fc78710329dadc131583691191f1f231d9bc5e9e87a9adf9ae86c7192def30d", "-o", "test.png", "--wait", "3000"])
