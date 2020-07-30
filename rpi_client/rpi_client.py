import pywifi
import requests
from time import sleep
from datetime import datetime

# Scan the nearby access points with given interface
def scan_wifi(iface):
    iface.scan()
    sleep(10)

    # Process the result of scanning
    result=iface.scan_results()
    # Reverse lookup table from pywifi
    akm_lookup_table = [
        "NONE",
        "WPA",
        "WPAPSK",
        "WPA2",
        "WPA2PSK",
        "UNKNOWN"
    ]
    result=[{
        'ssid': i.ssid,
        'bssid': i.bssid,
        'akm': [ akm_lookup_table[akm] for akm in i.akm],
        'freq': i.freq,
        'rssi': i.signal
    } for i in result]

    return result

wifi = pywifi.PyWiFi()

# Show all of the wireless interface to select.
interfaces = wifi.interfaces()
for (i,iface) in enumerate(interfaces):
  print(i, iface.name())
n_iface = -1
while(n_iface<0 or n_iface>=len(interfaces)):
    try:
        n_iface = int(input("Please select the interface number:"))
    except:
        pass

# Begin scanning at the selected interface
iface = interfaces[n_iface]
print("Selected interface", iface.name())
while(True):
    now = datetime.now()
    now = now.strftime("[%H:%M:%S]")
    print(now, "Begin scanning...")
    result = scan_wifi(iface)
    print("Scanning was completed. Result as follow.")
    for i in result:
        print('\t',i)
    r = requests.post('http://localhost:3000', json=result)
    print()
