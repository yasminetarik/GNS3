# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:47:07 2024

@author: HP
"""

import json

def generate_config(json_data, output_dir):
    
    for AS in json_data.keys(): 
        
        for router, config in json_data[AS]['routers'].items():
            
            with open(f"{output_dir}/{router}_config.txt", 'w') as file:
                file.write(f"! Configuration for {router}\n")
                file.write(f"hostname {router}\n\n")

                for interface in config['interfaces']:
                    file.write(f"interface {interface['interfaceName']}\n")
                    file.write(f" ip address {interface['ipAddress']} {interface['subnetMask']}\n")
                    file.write(" no shutdown\n\n")

                if 'RIP' in config:
                    file.write("router rip\n")
                    file.write(" version 2\n")
                    for network in config['RIP']['networks']:
                        file.write(f" network {network}\n")
                    file.write("\nno auto-summary\n\n")

                if 'OSPF' in config:
                    ospf_config = config['OSPF']
                    file.write("router ospf 1\n")
                    for network in ospf_config['networks']:
                        nw = network['network']
                        mask = network['wildcardMask']
                        area_id = network['area']
                        file.write(f" network {nw} {mask} area {area_id}\n")
                    file.write("\n")

                if 'iBGP' in config:
                    asn = json_data[AS]['autonomousSystem']
                    file.write(f"router bgp {asn}\n")
                    file.write(" bgp log-neighbor-changes\n")
                    for peer in config['iBGP']['peers']:
                        file.write(f" neighbor {peer} remote-as {asn}\n")
                    file.write("\n")

                if 'eBGP' in config:
                    asn_d = json_data[AS]['autonomousSystem']
                    file.write(f"router bgp {asn_d}\n")
                    for voisin in config["eBGP"]["neighbors"]:
                        asn_a = voisin["remoteAsn"]
                        neighbor = voisin["ipAddress"]
                        file.write(f" neighbor {neighbor} remote-as {asn_a}\n")
                    file.write("\n")

                file.write("!\n")

# Example usage
json_file = 'path_to_your_json_file.json'
output_directory = 'path_to_output_directory'

with open(json_file, 'r') as file:
    data = json.load(file)

generate_config(data, output_directory)

