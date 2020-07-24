
Knowledge Base: Basic Home Internet Troubleshooter

--- Explanation of Rules ---

I came up with the rules by first thinking of common issues with routers, modems, and 
network configuration. In the rules file, these issues are organized from least to most
complex to resolve.

The knowledge base works like a Windows troubleshooter - it is used when the user has no 
Internet access and returns a suggestion to fix the issue based on the information it is 
given.


--- Use Case Examples ---

User will input different things that they observe that will allow the knowledge base to
infer what the Internet issue might be caused by. The user should start by checking the
basic atoms - like router_has_power, router_lights_solid, public_IP_assigned, etc. These
atoms are contained in the first section of rules.

If the knowledge base can't infer the source of the issue from the basic atoms, the user
should check the more complex conditions in the second rule section - like modem_NAT, 
wired_connection, wifi_connection, etc.


Some atom meaning clarifications:

- have_local_IP: the host (user's machine) has a local IP address

- public_IP_assigned: the modem is in possession of a public IP from the ISP

- router_WAN_connected_to_modem: if there's an ethernet cable going from the router's WAN
                                 port to the modem

- public_IP_over_WAN: the modem is sending a public IP over the WAN port - i.e. plugging
                      the host into the modem will result in the host being assigned a 
                      public IP

- no_modem_NAT: the modem is not responsible for the Network Address Translation service

- modem_NAT: the modem is responsible for the Network Address Translation service

- no_SSID: the host cannot see an SSID being broadcast from the router

- wifi_connection: the host has established a connection to the router via WiFi

- wired_connection: the host is hardwired via Ethernet to the router

- can_ping_IP: the host can ping some external public IP address successfully

- cant_ping_hostname: the host cannot successfully ping a hostname, like www.google.ca
