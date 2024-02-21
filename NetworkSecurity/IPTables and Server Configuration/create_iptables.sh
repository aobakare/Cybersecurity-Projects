#!/bin/bash
#10.229.1.2 = windows host 
#10.229.1.1 = linux host

#set policy default to drop
#drop all packets coming in by default
iptables --policy INPUT DROP
#drop all packets to be forwarded by default
iptables --policy FORWARD DROP


#IPTABLE RULES
#Since i set the policies of input and forward chain to drop by default i have to write rules for what i want it to accept 
#http rules
#this will only accept fowarding of packets from .2.0/24 network to the windows host (this will make only those packets have access to the windows http server)
#--dport 80 specifies tcp destination port 80 which is for ttp
#--sport 80 specifies tcp source port 80 which is for ttp
iptables -A FORWARD -p tcp -s 10.229.2.0/24 -d 10.229.1.2 --dport 80 -j ACCEPT
iptables -A FORWARD -p tcp -s 10.229.1.2 -d 10.229.2.0/24 --sport 80 -j ACCEPT
#this will only allow packets coming in from 3.0/24 network to have acces to linux host http server 
iptables -A INPUT -p tcp -s 10.229.3.0/24 -d 10.229.1.1 --dport 80 -j ACCEPT

#ftp rules
#this will allow only packets cominng from the 3.0/24 network trying to connect to port 21 on the linux host, we use port 21 because this is the port reqiured for active ftp mode
iptables -A INPUT -p tcp -s 10.229.3.0/24 -d 10.229.1.1 --dport 21 -m state --state ESTABLISHED,NEW -j ACCEPT
#we only ever connect to port 20 if preexisting connection has been established which is why we used the ESTABLISJED key word here 
iptables -A INPUT -p tcp -s 10.229.3.0/24 -d 10.229.1.1 --dport 20 -m state --state ESTABLISHED -j ACCEPT
#this is for the passive mode i have not specified the port ranges in my config file, and the server assigns ports >1024 as destination to a RELATED/ESTABLISDHED connection(65535 is the maximum port number)
#RELATED  means the packet us starting a new connection but it s associated with an existing connection (such as an FTP data transfer)
iptables -A INPUT -p tcp -s 10.229.3.0/24 -d 10.229.1.1 --dport 1024:65535 -m state --state RELATED,ESTABLISHED -j ACCEPT
#resonses between the linux host and client are handled by default because my output policy is set to accept
#this will allow only packets going fromm 2.0/24 network trying to connect to the windows host 
#for active mode
#allow client to establish connection
iptables -A FORWARD -p tcp -s 10.229.2.0/24 -d 10.229.1.2 --dport 21 -m state --state ESTABLISHED,NEW -j ACCEPT
#allow server response
iptables -A FORWARD -p tcp -s 10.229.1.2 -d 10.229.2.0/24 --sport 21 -m state --state ESTABLISHED,RELATED -j ACCEPT
#allow transfer of data between the client and server 
iptables -A FORWARD -p tcp -s 10.229.1.2 -d 10.229.2.0/24 --sport 20 -m state --state ESTABLISHED -j ACCEPT 
iptables -A FORWARD -p tcp -s 10.229.2.0/24 -d 10.229.1.2 --dport 20 -m state --state ESTABLISHED -j ACCEPT 
#this is to allow transfer of data between server and client in passive mode
iptables -A FORWARD -p tcp -s 10.229.1.2 -d 10.229.2.0/24 --sport 1024:65535 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -p tcp -s 10.229.2.0/24 -d 10.229.1.2 --dport 1024:65535 -m state --state RELATED,ESTABLISHED -j ACCEPT

#ssh rules
#--dport 22 specifies port 22 which is used for ssh connections
#this will accept any packets coming from any host to connect to ssh on the linux host
iptables -A INPUT -p tcp -d 10.229.1.1 --dport 22 -j ACCEPT
iptables -A FORWARD -p tcp -s 10.229.1.1 --sport 22 -j ACCEPT 
#this will allow any packets trying to connect to ssh on the windows host be forwarded
iptables -A FORWARD -p tcp -d 10.229.1.2 --dport 22 -j ACCEPT 
iptables -A FORWARD -p tcp -s 10.229.1.2 --sport 22 -j ACCEPT 

#icmp rules
#this will allow icmp echo messages from any host be sent to both the windows and linux host
#--icmp-type 8 signifies echo request type 0 signifies echo replies
iptables -A INPUT -p icmp --icmp-type 8 -d 10.229.1.1 -j ACCEPT
iptables -A FORWARD -p icmp --icmp-type 8 -d 10.229.1.2 -j ACCEPT
iptables -A FORWARD -p icmp --icmp-type 0 -s 10.229.1.2 -j ACCEPT

#to allow host on our group internal network have access to our group host services 
iptables -A INPUT -s 10.229.1.0/24 -d 10.229.1.1 -j ACCEPT
iptables -A FORWARD -s 10.229.1.0/24 -d 10.229.1.2 -j ACCEPT

#outbound restrictions
#this will drop any packets from the windows host trying to access services of any host on the 2.0/24 network
iptables -A OUTPUT -s 10.229.1.2 -d 10.229.2.0/24 -m state --state NEW -j DROP

# LOG VIOLATION OF RULES ls
# -N creates a chain "LOGINPUT"
# Remaining INPUT packets go to LOGINPUT
# The limit module is added to regualte the number of logs. We have specified an average number of 10 logs per minute and the maximum burst as 15
# Drop the packets that came to LOGINPUT
iptables -N LOGINPUT
iptables -A INPUT -j LOGINPUT
iptables -A LOGINPUT -m limit --limit 10/m --limit-burst 15 -j LOG --log-prefix "INPUT traffic logged: "
iptables -A LOGINPUT -j DROP
#
# Same as above, but for logging FORWARD packets
iptables -N LOGFORWARD
iptables -A FORWARD -j LOGFORWARD
iptables -A LOGFORWARD -m limit --limit 10/m --limit-burst 15 -j LOG --log-prefix "FORWARD traffic logged: "
iptables -A LOGFORWARD -j DROP
#
#Log violations of the outbound restriction
iptables -N LOGOUTPUT
iptables -A OUTPUT -s 10.229.1.2 -d 10.229.2.0/24 -m state --state NEW -j LOGOUTPUT
iptables -A LOGOUTPUT -m limit --limit 10/m --limit-burst 15 -j LOG --log-prefix "OUTPUT traffic logged: "
iptables -A LOGOUTPUT -j DROP
