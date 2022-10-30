import ipaddress
import re

#[+] ----- FUNCTIONS BLOCK ----- [+]
### IP2Location database converter ###
def long2DotIP(ipnum):
    return str(int(ipnum / 16777216) % 256) + "." + str(int(ipnum / 65536) % 256) + "." + str(int(ipnum / 256) % 256) + "." + str(ipnum % 256)
#example : print(long2DotIP(1201147904))

def dot2LongIP(ip):
    return int(ipaddress.IPv4Address(ip))
#example : print(long2DotIP(1.1.1.0))


#[+] ----- CODE BLOCK ----- [+]
### Convert all database long 2 readable IPs
filepath = 'C:/temp/test_ip.txt'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        parsed_long = re.findall(r'"([^"]*)"', line)[0]

        print(long2DotIP(int(parsed_long)))

        line = fp.readline()
        cnt += 1



### GET IP from /var/log/access.log ###
# /// TO COMPLETE ///
### ###

### Extract latitude / longitude from IP field
# /// TO COMPLETE ///
### ###

### Get timestamp
# /// TO COMPLETE ///
### ###


#[+] ----- DATABASE BLOCK ----- [+]
###### Add all fields into MySQL local database ######
# /// TO COMPLETE ///

###### ######