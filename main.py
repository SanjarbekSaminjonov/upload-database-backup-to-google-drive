import os

import environs
import requests

env = environs.Env()
env.read_env()

bot_token = env.str("BOT_TOKEN")
chat_id = env.str("CHAT_ID")
url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

name = f"backup_2pay.uz.sql.gz"
file_path = os.curdir + f"/{name}"

command = f"""docker exec -t web_db pg_dumpall -c -U two_pay_user | gzip > {name}"""
os.system(command)

with open(file_path, "rb") as file:
    res = requests.post(
        url, files={"document": (file.name, file)}, data={"chat_id": chat_id}
    )
    print(res.text)

os.remove(name)
