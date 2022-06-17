# #This file will contain all the networking side of the project
# # This functions finds a device connected using the DHCP- ACK flag
# from scapy.all import sniff

# def deviceConnected():
#     # TODO
#     return 0
# NEW ##########################################################################
#!/usr/bin/env python3
"""scapy-dhcp-listener.py

Listen for DHCP packets using scapy to learn when LAN 
hosts request IP addresses from DHCP Servers.

Copyright (C) 2018 Jonathan Cutrer

License Dual MIT, 0BSD

"""

from __future__ import print_function
from scapy.all import *
import time
from fingerPrintDevice import deviceInfo
from SeniorProject import sndMessage

__version__ = "0.0.3"

# print(f"Host {hostname} ({packet[Ether].src}) requested {requested_addr}")

#format_info pretties up DeviceName, Mac Address, IP Address, and Open Ports from ELSEIF REQUEST PACKET.
def format_info(host_name, mac_name,ip):
    host = host_name
    mac_address = mac_name
    ip_address = ip
    open_ports = ""
    version_info = ""

    return ("Host Name:" + host + "\n" + "Mac Address:" + mac_address + "\n" + "IP Address:" + ip_address + "\n" + "Open Ports:" + open_ports + "\n" + "Version:" + version_info)


# Fixup function to extract dhcp_options by key
def get_option(dhcp_options, key):

    must_decode = ['hostname', 'domain', 'vendor_class_id']
    try:
        for i in dhcp_options:
            if i[0] == key:
                # If DHCP Server Returned multiple name servers 
                # return all as comma seperated string.
                if key == 'name_server' and len(i) > 2:
                    return ",".join(i[1:])
                # domain and hostname are binary strings,
                # decode to unicode string before returning
                elif key in must_decode:
                    return i[1].decode()
                else: 
                    return i[1]        
    except:
        pass


def handle_dhcp_packet(packet):

    # Match DHCP DISCOVER PACKET
    if DHCP in packet and packet[DHCP].options[0][1] == 1:
        print('---')
        print('New DHCP Discover')
        #print(packet.summary())
        #print(ls(packet))
        hostname = get_option(packet[DHCP].options, 'hostname')
        print(f"Host {hostname} ({packet[Ether].src}) asked for an IP")


    # Match DHCP OFFER PACKET
    elif DHCP in packet and packet[DHCP].options[0][1] == 2:
        print('---')
        print('New DHCP Offer')

        subnet_mask = get_option(packet[DHCP].options, 'subnet_mask')
        lease_time = get_option(packet[DHCP].options, 'lease_time')
        router = get_option(packet[DHCP].options, 'router')
        name_server = get_option(packet[DHCP].options, 'name_server')
        domain = get_option(packet[DHCP].options, 'domain')

        print(f"DHCP Server {packet[IP].src} ({packet[Ether].src}) "
              f"offered {packet[BOOTP].yiaddr}")

        print(f"DHCP Options: subnet_mask: {subnet_mask}, lease_time: "
              f"{lease_time}, router: {router}, name_server: {name_server}, "
              f"domain: {domain}")


    # Match DHCP REQUEST PACKET
    elif DHCP in packet and packet[DHCP].options[0][1] == 3:
        print('---')
        print('New DHCP Request')

        requested_addr = get_option(packet[DHCP].options, 'requested_addr')
        hostname = get_option(packet[DHCP].options, 'hostname')
        ## TODO
        ## Lets edit this to scan for the IP
        print("Loading you litte shit\nSacnning ...",str(requested_addr))
        time.sleep(5)
        print(deviceInfo(str(requested_addr)))
        print("Scanninf Done Bitch!!")
        print(f"Host {hostname} ({packet[Ether].src}) requested {requested_addr}")  #hostname = hostname, packet[Ether].src = mac address, requested_addr = ip address
        text_message = format_info(str(hostname),str(packet[Ether].src), str(requested_addr))
        sndMessage(text_message)

    # Match DHCP ACK PACKET
        
        # elif DHCP in packet and packet[DHCP].options[0][1] == 5:
        # print('---')
        # print('New DHCP Ack')

        # subnet_mask = get_option(packet[DHCP].options, 'subnet_mask')
        # lease_time = get_option(packet[DHCP].options, 'lease_time')
        # router = get_option(packet[DHCP].options, 'router')
        # name_server = get_option(packet[DHCP].options, 'name_server')
        # ## TODO
        # ## Lets edit this to scan for the IP
        # print("Loading you litte shit\nSacnning ...",str(packet[BOOTP].yiaddr))
        # time.sleep(5)
        # print(deviceInfo(str(packet[BOOTP].yiaddr)))
        # print("Scanninf Done Bitch!!")

        # print(f"DHCP Server {packet[IP].src} ({packet[Ether].src}) "
        #       f"acked {packet[BOOTP].yiaddr}")

        # print(f"DHCP Options: subnet_mask: {subnet_mask}, lease_time: "
        #       f"{lease_time}, router: {router}, name_server: {name_server}")
        
    # Match DHCP INFORM PACKET
    elif DHCP in packet and packet[DHCP].options[0][1] == 8:
        print('---')
        print('New DHCP Inform')

        hostname = get_option(packet[DHCP].options, 'hostname')
        vendor_class_id = get_option(packet[DHCP].options, 'vendor_class_id')

        print(f"DHCP Inform from {packet[IP].src} ({packet[Ether].src}) "
              f"hostname: {hostname}, vendor_class_id: {vendor_class_id}")

    else:
        print('---')
        print('Some Other DHCP Packet')
        print(packet.summary())
        print(ls(packet))

    return

if __name__ == "__main__":
    sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp_packet)