from __future__ import print_function
from scapy.all import *
import time
from fingerPrintDevice import deviceInfo
from SeniorProject import sndMessage


#format_info pretties up DeviceName, Mac Address, IP Address, and Open Ports from ELSEIF REQUEST PACKET.
def format_info(hostname_name, mac_name,ip, nmap_info):
    hostname = hostname_name
    mac_address = mac_name
    ip_address = ip
    open_ports = ""
    version_info = ""

    return ("hostname Name:" + hostname + "\n" + "Mac Address:" + mac_address + "\n" + "IP Address:" + ip_address + "\n" + "Open Ports:" + open_ports + "\n" + "Version:" + version_info + "Nmap info: " + nmap_info)

#Ricardo's Banner vendor_class_idS start
def banner_start():
    logo = '''
    ____  _                     __         ________  _____
   / __ \(_)________ __________/ /___     /  _/ __ \/ ___/
  / /_/ / / ___/ __ `/ ___/ __  / __ \    / // / / /\__ \ 
 / _, _/ / /__/ /_/ / /  / /_/ / /_/ /  _/ // /_/ /___/ / 
/_/ |_/_/\___/\__,_/_/   \__,_/\____/  /___/_____//____/  
                                                          
'''
    temp = "hello"
    return(logo)

# Function finds DCHP flag
def options(dhcp_flags, flag_type):

    must_decode = ['hostname', 'domain', 'vendor_class_id']
    try:
        for i in dhcp_flags:
            if i[0] == flag_type:

                if flag_type == 'name_server' and len(i) > 2:
                    return ",".join(i[1:])

                elif flag_type in must_decode:
                    return i[1].decode()
                else: 
                    return i[1]        
    except:
        pass

def dhcp_listener(packet):

    # I will listen in to get DHCP discover
    if DHCP in packet and packet[DHCP].options[0][1] == 1:
        print('---')
        print('New DHCP Discover')
        hostname = options(packet[DHCP].options, 'hostname')
        print(f"hostname {hostname} ({packet[Ether].src}) asked for an IP")


    # I will listen in to get DHCP offer
    elif DHCP in packet and packet[DHCP].options[0][1] == 2:
        print('---')
        print('New DHCP Offer')

        subnet_mask = options(packet[DHCP].options, 'subnet_mask')
        lease_time = options(packet[DHCP].options, 'lease_time')
        router = options(packet[DHCP].options, 'router')
        name_server = options(packet[DHCP].options, 'name_server')
        domain = options(packet[DHCP].options, 'domain')


    # I will listen in to a DHCP request packet
    elif DHCP in packet and packet[DHCP].options[0][1] == 3:
        print('---')
        print('New DHCP Request')

        requested_addr = options(packet[DHCP].options, 'requested_addr')
        hostname = options(packet[DHCP].options, 'hostname')
        print("Loading and Scanning ...",str(requested_addr))
        time.sleep(5)
        device = (deviceInfo(str(requested_addr)))
        print("Scanning Done!!")
        print(f"hostname {hostname} ({packet[Ether].src}) requested {requested_addr}" ,device)  #hostname = hostname, packet[Ether].src = mac address, requested_addr = ip address
        text_message = format_info(str(hostname),str(packet[Ether].src), str(requested_addr), str(device))
        sndMessage(text_message)


if __name__ == "__main__":
    print(banner_start())
    sniff(filter="udp and (port 67 or 68)", prn=dhcp_listener)
