import ipaddress
import re
import time, os

#[+] ----- IP FUNCTIONS BLOCK ----- [+]
### IP2Location database converter ###
def long2DotIP(ipnum):
    return str(int(ipnum / 16777216) % 256) + "." + str(int(ipnum / 65536) % 256) + "." + str(int(ipnum / 256) % 256) + "." + str(ipnum % 256)
#example : print(long2DotIP(1201147904))

def dot2LongIP(ip):
    return int(ipaddress.IPv4Address(ip))
#example : print(long2DotIP(1.1.1.0))


#[+] ----- CODE BLOCK ----- [+]
### Convert all database 'long' 2 'readable' IPs
filestream_path = 'C:/temp/test_ip.txt'
answer_path = 'C:/temp/answer_ip.txt'
with open(filestream_path, 'r') as filestream:
    with open(answer_path, 'w') as answer:
        for line in filestream:
            currentline = line.split(',') # Split format of out-file
            
            total = str((long2DotIP(int((currentline[0]).replace('"','')))) + ', ' + (long2DotIP(int((currentline[1]).replace('"','')))) + ', ' + currentline [6] + ', ' + currentline[7]) + "\n"
            
            #print(total)
            answer.write(total)


### GET IP from /var/log/access.log ###
# /// TO COMPLETE ///
### ###

# Read in live nginx log file
file = open('/var/log/nginx/access.log', mode='r')
i = 1
while 1:
#       where = file.tell()
        line = file.readline()
        if not line:
                time.sleep(0.5)
                #file.seek(where)
        else:
                print(line)
                #Block to add retrieve IP and add in database a value
                i = i + 1
                print(i)


### Extract latitude / longitude from IP field
# /// TO COMPLETE ///
### ###


#[+] ----- DATABASE BLOCK ----- [+]
###### Add all fields into MySQL local database ######
# /// TO COMPLETE ///

###### ######