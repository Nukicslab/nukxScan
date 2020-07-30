import pywifi
from time import sleep

wifi = pywifi.PyWiFi()

for (i,iface) in enumerate(wifi.interfaces()):
  print(i, iface.name())
n_iface = int(input("Please select the interface number:"))

iface = wifi.interfaces()[n_iface]
iface.scan()

sleep(10)

result=iface.scan_results()

for i in result:
    print(i.__dict__)