#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import csv
from dotenv import load_dotenv
import os  
import socket

def main():
    import ipaddress

    def ip_range(start_ip, end_ip):
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]

    with open('ips_and_ranges.txt', 'r') as file:
        lines = file.readlines()

    all_ips = []  # Initialize a list to store all IPs

    for line in lines:
        line = line.strip()
        if '-' in line:
            start_ip, end_ip = line.split(' - ')
            for ip in ip_range(start_ip, end_ip):
                all_ips.append(ip)  # Add each IP to the list
        elif '/' in line:
            network = ipaddress.ip_network(line, strict=False)
            for ip in network:
                all_ips.append(str(ip))  # Add each IP to the list
        else:
            all_ips.append(line)  # Add the single IP to the list

    for ip in all_ips:
        load_dotenv()
        token = os.getenv('IPINFO_API_TOKEN')
        url = f"https://ipinfo.io/{ip}/json?token={token}"
        response = requests.get(url)
        data = response.json()

        with open('ip_details.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                data.get('ip'), data.get('hostname'), data.get('city'), 
                data.get('region'), data.get('country'), data.get('loc'), 
                data.get('org'), data.get('postal'), data.get('timezone')
            ])


if __name__ == "__main__":
    main()
    exit()

