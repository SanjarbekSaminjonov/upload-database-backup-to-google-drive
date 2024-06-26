import os
import environs

from drive import file_upload

# get env object
env = environs.Env()
env.read_env()

# get variables
BOT_TOKEN = env.str("BOT_TOKEN")
CHAT_ID = env.str("CHAT_ID")
current_dir = env.str("CURRENT_DIR")
db_name = env.str("DB_NAME")
db_user = env.str("DB_USER")
backup_name = f"{db_name}_{db_user}.sql.gz"

# change dir to project root
os.chdir(current_dir)

# dump database
command = f"docker exec -t {db_name} pg_dumpall -c -U {db_user} | gzip > {backup_name}"
os.system(command)

# upload backup file to drive
file = file_upload(backup_name, "application/gz")

# send message to telegram
message = (
    f"Database backup: <code>{file}</code>\n\n"
    f"File name: \t<b>{backup_name}</b>\n"
    f"File size: \t<b>{round(os.path.getsize(backup_name) / 2**20, 2)} MB</b>"
)
command = f"curl -s -X POST https://api.telegram.org/bot{BOT_TOKEN}/sendMessage -d chat_id={CHAT_ID} -d text='{message}' -d parse_mode=HTML"
os.system(command)

# delete backup file from server
os.remove(backup_name)
