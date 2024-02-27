import os
import datetime

import environs
import requests

env = environs.Env()
env.read_env()

bot_token = env.str("BOT_TOKEN")
chat_id = env.str("CHAT_ID")
url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

name = f"backup_2pay.uz_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
file_path = os.curdir + f"/{name}"

os.system(f"docker exec -t web_db pg_dumpall -c -U two_pay_user > {name}")

with open(file_path, "rb") as file:
    files = {"document": (file.name, file)}
    data = {"chat_id": chat_id, "caption": "this is backup"}
    res = requests.post(url, files=files, data=data)
    print(res.text)

os.remove(name)
