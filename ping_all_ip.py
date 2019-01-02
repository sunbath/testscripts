# Author: Eric Leung
# Purpose: To ping all hosts in a given IPv4 Network to see if host is online.
# Last Modified Date: 31-Dec-2018

# Import modules
import subprocess
import ipaddress
import socket

# Function call to lookup address
def lookup(addr):
	try:
		return socket.gethostbyaddr(addr)
	except socket.herror:
		return None, None, None

def main():
	# Create the network
	ip_net = ipaddress.ip_network(u"192.168.73.0/24")

	# Get all hosts on that network
	all_hosts = list(ip_net.hosts())

	num_online_host = 0
	num_offline_host = 0

	# For each IP address in the subnet, 
	# run the ping command with subprocess.popen interface
	for i in range(len(all_hosts)):
	    output = subprocess.Popen(['ping', '-c', '1', '-W', '1', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()[0]
	    hostname,alias,addresslist = lookup(str(all_hosts[i]))
	    
	    if "100% packet loss" in output.decode('utf-8'):
	        print str(all_hosts[i]), "is Offline. \tHostname: ", str(hostname)
	        num_offline_host += 1
	    #elif "Request timed out" in output.decode('utf-8'):
	    #    print str(all_hosts[i]), "is Offline"
	    else:
	        num_online_host += 1
	        print str(all_hosts[i]), "is Online. \tHostname: ", str(hostname)

	total_hosts = num_online_host +  num_offline_host

	print "\n"
	print "Total Number of Hosts: \t\t", total_hosts
	print "Number of Hosts Online: \t", num_online_host
	print "Number of Hosts Offline: \t", num_offline_host

if __name__ == "__main__":
	main()
