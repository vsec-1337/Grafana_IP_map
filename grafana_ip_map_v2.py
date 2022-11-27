import ipaddress
from ipregistry import IpregistryClient
import mysql.connector
from mysql.connector import Error
import time



##### --- User input definition block --- #####

host = input(""" What is the Hostname / IP of the Database Server ?
ex : 10.13.120.53
> """)

database = input(""" What is the databse name on the Database Server ?
ex : grafana_map
> """)

user = input(""" What is the username to use on the Database Server connection ?
ex : grafana_consult
> """)

password = input(""" What is the password to use on the Database Server connection ?
ex : your_secure_password
> """)

api_key = input(""" What is your ipregistry api key ?
get it on : https://ipregistry.co
> """)

# Resume user configuration
print ("[+] The database host will be : " + host,
'\n' + "[+] The database will be : " + database,
'\n' + "[+] The database user will be : " + user,
'\n' + "[+] The database password will be : " + password,
'\n' + "[+] The api key will be : " + api_key)



##### --- Global functions/variables declaration --- #####

# SQL connector
connection = mysql.connector.connect(host,
                                     database,
                                     user,
                                     password)

# IPregistry API key
client = IpregistryClient(api_key)

# Function to search if a value exist on a specific SQL table
def select_query(ip_select, table_select):
    cursor = connection.cursor(buffered=True)
    result = cursor.execute("SELECT * FROM " + table_select + " where IP like '" + ip_select + ".%'")
    row = cursor.fetchone()
    cursor.close()
    return row

# Function to insert a value on a specific SQL table
def insert_query(table_insert, ip_insert, latitude_insert, longitude_insert):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO " + table_insert + " (IP, latitude, longitude) VALUES ('" + ip_insert + "', '" + latitude_insert + "', '" + longitude_insert + "')")
    connection.commit()
    cursor.close()

# Function used to get latitude and longitude of a unknown IP (use ipregistry API key : https://ipregistry.co)
def api_query(ip_api):
    ipInfo = client.lookup(ip_api)
    return str(ipInfo.ip), str(ipInfo.location["latitude"]), str(ipInfo.location["longitude"])



##### --- Instructions block --- #####

# This block will read all new lines in your NGINX access log file : /var/log/nginx/access.log
with open('/var/log/nginx/access.log', 'r') as file:
    while 1:
        time.sleep(0.05) # /!\ This value can be modify to increase or reduce process CPU utilisation /!\
        for line in file.readlines():
            d = dict()
            # split only work if values are separated by ' - - ' in .log file. Modify nginx log format in /etc/nginx/nginx.conf to meet this requirement
            d = line.split(' - - ')[0]
            ip_split = d.split('.')[0] + '.' + d.split('.')[1] + '.' + d.split('.')[2]

            # Exit this value if the current IP is a private or a localhost one
            if (d.split('.')[0] == "10") or (d.split('.')[0]=="127") or (d.split('.')[0]=="192"):
                continue
            
            # Check if the IP is in "cache" SQL table
            row = select_query(ip_split, "cache_ips")
            if row:
                insert_query("live_ips", row[0], row[1], row[2])
            else:
                # Check if the IP is in "source" SQL table
                row = select_query(ip_split, "source_ips")
                if row:
                    insert_query("cache_ips", row[0], row[1], row[2])
                    insert_query("live_ips", row[0], row[1], row[2])
                else:
                    # Exit this value if the IP is an IPv6 one
                    if (len(d)>15):
                        continue
                    else:
                        # Query IPregistry API to get lat and Lon. Insert all these informations into "source", "cache" and "live" SQL tables
                        api_value = api_query(d)
                        insert_query("source_ips", api_value[0], api_value[1], api_value[2])
                        insert_query("cache_ips", api_value[0], api_value[1], api_value[2])
                        insert_query("live_ips", api_value[0], api_value[1], api_value[2])