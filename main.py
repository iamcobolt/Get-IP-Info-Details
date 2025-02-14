#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import csv
from dotenv import load_dotenv
import os
import socket
from datetime import datetime

def main():
    import ipaddress

    def ip_range(start_ip, end_ip):
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]

    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    # Create CSV with headers
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'ip_details.csv'
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'IP', 'Hostname', 'City', 'Region', 'Country', 'Location',
            'Organization', 'Postal', 'Timezone', 'Country Name', 'Country Code',
            'Region Code', 'EU Country', 'Continent', 'Latitude', 'Longitude',
            'Metro Code', 'Area Code', 'ASN', 'ASN Name', 'Company Name',
            'Company Domain', 'Company Type', 'Company Registry', 'Company Registry Page',
            'Privacy Proxy', 'Privacy VPN', 'Privacy Tor', 'Privacy Relay',
            'Privacy Hosting', 'Abuse Contact Name', 'Abuse Contact Email',
            'Abuse Contact Phone', 'Abuse Contact Network', 'Abuse Contact Country',
            'Domains', 'Carrier Name', 'Carrier MCC', 'Carrier MNC'
        ])

    # Load environment variables once
    load_dotenv()
    token = os.getenv('IPINFO_API_TOKEN')

    with open('ips_and_ranges.txt', 'r') as file:
        lines = file.readlines()

    all_ips = []  # Initialize a list to store all IPs

    for line in lines:
        line = line.strip()
        if '-' in line:
            start_ip, end_ip = line.split(' - ')
            for ip in ip_range(start_ip, end_ip):
                all_ips.append(ip)
        elif '/' in line:
            network = ipaddress.ip_network(line, strict=False)
            for ip in network:
                all_ips.append(str(ip))
        else:
            all_ips.append(line)

    total_ips = len(all_ips)
    for index, ip in enumerate(all_ips, 1):
        print(f"Processing IP {index}/{total_ips}: {ip}")
        
        try:
            url = f"https://ipinfo.io/{ip}/json?token={token}"
            response = requests.get(url)
            data = response.json()

            # Extract location coordinates
            loc = data.get('loc', '').split(',')
            latitude = loc[0] if len(loc) > 0 else ''
            longitude = loc[1] if len(loc) > 1 else ''

            # Get additional data from nested structures
            company = data.get('company', {})
            abuse = data.get('abuse', {})
            privacy = data.get('privacy', {})
            asn = data.get('asn', {})
            carrier = data.get('carrier', {})

            with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    data.get('ip'),
                    data.get('hostname'),
                    data.get('city'),
                    data.get('region'),
                    data.get('country'),
                    data.get('loc'),
                    data.get('org'),
                    data.get('postal'),
                    data.get('timezone'),
                    data.get('country_name'),
                    data.get('country_code'),
                    data.get('region_code'),
                    data.get('is_eu'),
                    data.get('continent'),
                    latitude,
                    longitude,
                    data.get('metro'),
                    data.get('area_code'),
                    asn.get('asn'),
                    asn.get('name'),
                    company.get('name'),
                    company.get('domain'),
                    company.get('type'),
                    company.get('registry'),
                    company.get('registry_page'),
                    privacy.get('proxy'),
                    privacy.get('vpn'),
                    privacy.get('tor'),
                    privacy.get('relay'),
                    privacy.get('hosting'),
                    abuse.get('name'),
                    abuse.get('email'),
                    abuse.get('phone'),
                    abuse.get('network'),
                    abuse.get('country'),
                    data.get('domains'),
                    carrier.get('name'),
                    carrier.get('mcc'),
                    carrier.get('mnc')
                ])

        except Exception as e:
            print(f"Error processing IP {ip}: {str(e)}")
            continue

    print(f"\nProcessing complete! Results saved to {csv_filename}")

if __name__ == "__main__":
    main()

