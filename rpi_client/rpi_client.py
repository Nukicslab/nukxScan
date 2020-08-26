import pywifi
import requests
import socket # For getting hostname
import time
from time import sleep
from datetime import datetime

# Scan the nearby access points with given interface
def scan_wifi(iface):
    iface.scan()
    sleep(5)

    # Process the result of scanning
    result=iface.scan_results()
    # Reverse lookup table from pywifi
    akm_lookup_table = [
        "NONE",
        "WPA",
        "WPA_PSK",
        "WPA2",
        "WPA2_PSK",
        "UNKNOWN"
    ]
    result=[{
        # Convert to UTF-8
        'ssid': i.ssid.encode().decode('unicode-escape').encode('latin1').decode('utf-8'),
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
n_iface = 0

# Begin scanning at the selected interface
iface = interfaces[n_iface]
print("Selected interface", iface.name())
upload_url = 'http://172.16.0.1:3000/update'
while(True):
    
    scan_time = datetime.now()
    scan_time_str = scan_time.strftime("[%H:%M:%S]")

    # Convert to Javascript timestamp
    scan_time_timestamp = int(time.mktime(scan_time.timetuple()))
    scan_time_timestamp *= 1000

    print(scan_time_str, "Begin scanning...")
    result = scan_wifi(iface)
    
    print("Scanning was completed. Result as follow.")
    for i in result:
        print('\t',i)
    
    # Data the will upload to IoT server
    upload_data = {
        'time': scan_time_timestamp,
        'hostname': socket.gethostname(),
        'result': result
    }
    
    r = requests.post(upload_url, json=upload_data)
    if(r.status_code == 200):
        print("Uploading result was completed.")
    print()
