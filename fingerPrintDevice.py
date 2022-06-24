# We are using nmap to scan the host
import nmap
# This just takes an IP address and return the device info i.e Open port or Operating system
def deviceInfo(ipAddress):
    nm = nmap.PortScanner()
    nm.scan(ipAddress, arguments='-Pn -O -sV -A')
    return (nm.csv())

# print("IDS is loading")
#For debugging purposes
#print(deviceInfo('192.168.1.22'))