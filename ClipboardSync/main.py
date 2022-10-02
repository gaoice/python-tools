import configparser
import time
import utils

# python3

# 读取配置
config = configparser.RawConfigParser()
config.read("sync.ini", encoding='UTF-8')

host = config.get("DEFAULT", "host")
port = config.get("DEFAULT", "port")
user = config.get("DEFAULT", "user")
pw = config.get("DEFAULT", "password")
db = config.get("DEFAULT", "database")
table = config.get("DEFAULT", "table")
sleep_time = config.get("DEFAULT", "sleep_time")

last_text = b''
text = b''

clipboard = utils.ClipboardHelper
mysql = utils.MysqlHelper(host, port, user, pw, db, table)

# 初始化数据库
mysql.init_table()

while True:
    text = clipboard.get_text(last_text)
    # 本机更改
    if text != last_text:
        last_text = text
        mysql.set_text(text)
        print("本机剪切板更改")
    # 检测远程更改
    else:
        if mysql.is_changed():
            text = mysql.get_text()
            last_text = text
            clipboard.set_text(text)
            print("远程剪切板更改")
    # sleep
    time.sleep(int(sleep_time))
