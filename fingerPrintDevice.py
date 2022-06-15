# We are using nmap to scan the host
import nmap
# This just takes an IP address and return the device info i.e Open port or Operating system
def deviceInfo(ipAddress):
    nm = nmap.PortScanner()
    nm.scan(ipAddress, arguments='-Pn -O -sV -A')
    return (nm.csv())
# You can change this IP to anything for now
print(deviceInfo('192.168.1.93'))