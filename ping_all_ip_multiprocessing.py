# Filename: ping_all_ip_multiprocessing.py
# Author: Eric Leung
# Purpose: To ping all hosts in a given IPv4 Network to see if host is online and the task run in multiprocessesing
# Last Modified Date: 5-Jan-2019

# Import modules
import subprocess
import ipaddress
import socket
import re
import datetime

from multiprocessing import Pool

# Function call to lookup address
def lookup(addr):
    # Function to perform DNS Lookup
    try:
        return socket.gethostbyaddr(str(addr))
    except socket.herror:
        return None, None, None

def ping(addr):
    # Function to issue ping to host and perform ARP lookup if the host is reachable.

    ping_output = subprocess.Popen(['ping', '-c', '1', '-W', '0.2', str(addr)], stdout=subprocess.PIPE).communicate()[0]

    if "100.0% packet loss" in ping_output.decode('utf-8'):
        return "Offline", "N/A"
    else:
        arp_output = subprocess.Popen(['arp', '-n', str(addr)], stdout=subprocess.PIPE).communicate()[0]
        p = re.compile('([0-9a-fA-F]{1,2}(:|-)){5}([0-9a-fA-F]{1,2})')
        mac = re.search(p,str(arp_output))
        MAC_Address = mac.group(0)
        return "Online" , MAC_Address

def print_result(addr,ping_result,arp,hostname):
    # Function to print out the IP address, Ping Result, MAC Address and its hostname (one line at a time)

    #Color Codes for Text Format
    W = '\033[0m'   # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan

    if ping_result == "Online":
        print(f"{G}{addr} \t{G}{ping_result} \t\t{G}{arp} \t\t\t{G}{hostname}{W}")
    elif ping_result == "Offline":
        print(f"{R}{addr} \t{R}{ping_result} \t{R}{arp} \t\t\t\t\t\t{R}{hostname}{W}")

def main():

    # Record start time
    starttime = datetime.datetime.now()

    # Create the network
    ip_net = ipaddress.ip_network(u"192.168.11.0/24")

    # Get all hosts on that network
    all_hosts = list(ip_net.hosts())

    # Initalize variables to count the number of hosts
    num_online_host = 0
    num_offline_host = 0

    # Initalize multiprocessing pool and spawn the subprocesses based on the number of IPs
    ping_Pool = Pool(processes=len(all_hosts))
    dns_Pool = Pool(processes=len(all_hosts))


    print("Scanning in progress...")

    # Map the ping and dnslookup function to the pool with variables
    # Store the result to ping_result and dns_result as List
    ping_result = ping_Pool.map(ping, [host for host in all_hosts])
    dns_result = dns_Pool.map(lookup,[host for host in all_hosts])
    ping_Pool.close()
    dns_Pool.close()

    #Print the result and count the hosts
    print(f"IP \t\t\t\tStatus \t\tMAC Address \t\t\t\tHostname")
    print(f"-"*70)
    for i in range(len(all_hosts)):
        print_result(all_hosts[i],ping_result[i][0],ping_result[i][1],dns_result[i][0])
        if ping_result[i][0] == "Online":
            num_online_host += 1
        else:
            num_offline_host += 1

    total_hosts = num_online_host + num_offline_host

    print(f"\n")
    print(f"-" * 70)
    print(f"Number of Hosts Online: \t{num_online_host}")
    print(f"Number of Hosts Offline: \t{num_offline_host}")
    print(f"Total Number of IP: \t\t{total_hosts}")
    print(f"-" * 70)

    endtime = datetime.datetime.now()
    print(f"Result generated at {endtime}")
    print(f"Scan finished in {endtime-starttime}")
    print(f"-" * 70)

if __name__ == "__main__":
    main()
