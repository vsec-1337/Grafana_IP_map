import ipaddress
from ipregistry import IpregistryClient
import mysql.connector
from mysql.connector import Error
import time

connection = mysql.connector.connect(host='10.13.120.53',
                                             database='grafana_map',
                                             user='grafana_consult',
                                             password='GrafanaConsult./74')

def select_query(ip_select, table_select):
    cursor = connection.cursor(buffered=True)
    result = cursor.execute("SELECT * FROM " + table_select + " where IP like '" + ip_select + ".%'")
    row = cursor.fetchone()
    cursor.close()
    return row

def insert_query(table_insert, ip_insert, latitude_insert, longitude_insert):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO " + table_insert + " (IP, latitude, longitude) VALUES ('" + ip_insert + "', '" + latitude_insert + "', '" + longitude_insert + "')")
    connection.commit()
    cursor.close()

def api_query(ip_api):
    client = IpregistryClient("b3jnmgcxzr4hs5av")
    ipInfo = client.lookup(ip_api)
    return str(ipInfo.ip), str(ipInfo.location["latitude"]), str(ipInfo.location["longitude"])

with open('/var/log/nginx/access.log', 'r') as file:
    while 1:
        time.sleep(0.1)
        for line in file.readlines():
            d = dict()
            d = line.split(' - - ')[0]
            ip_split = d.split('.')[0] + '.' + d.split('.')[1] + '.' + d.split('.')[2]

            row = select_query(ip_split, "cache_ips")
            if row:
                insert_query("live_ips", row[0], row[1], row[2])
            else:
                row = select_query(ip_split, "source_ips")
                if row:
                    insert_query("cache_ips", row[0], row[1], row[2])
                    insert_query("live_ips", row[0], row[1], row[2])
                else:
                    insert_query("source_ips", api_query(d)[0], api_query(d)[1], api_query(d)[2])
                    insert_query("cache_ips", api_query(d)[0], api_query(d)[1], api_query(d)[2])
                    insert_query("live_ips", api_query(d)[0], api_query(d)[1], api_query(d)[2])