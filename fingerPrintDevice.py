# We are using nmap to scan the host
import nmap
# This just takes an IP address and return the device info i.e Open port or Operating system
def deviceInfo(ipAddress):
    nm = nmap.PortScanner()
    nm.scan(ipAddress, arguments='-Pn -O -sV -A')
    return (nm.csv())
# You can change this IP to anything for now
def prettyString(dInfo):
    #TODO 
    #Ricardo
    return(0)

print("Loading you litte shit")
print(deviceInfo('192.168.1.7'))