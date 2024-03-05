import os

import environs
import requests

env = environs.Env()
env.read_env()

bot_token = env.str("BOT_TOKEN")
chat_id = env.str("CHAT_ID")
url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

file_path = "/home/two_pay/backup_service/two_pay_backup.sql.gz"

os.chdir("/home/two_pay/backup_service/")
command = "docker exec -t web_db pg_dumpall -c -U two_pay_user | gzip > two_pay_backup.sql.gz"
os.system(command)

with open(file_path, "rb") as file:
    res = requests.post(
        url, files={"document": (file.name, file)}, data={"chat_id": chat_id}
    )
    print(res.text)

os.remove(file_path)
