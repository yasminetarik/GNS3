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
                    file.write(f" ip address {interface['ipAddress']}\n")
                    file.write(" no shutdown\n\n")

                if 'RIP' in config:
                    file.write("ipv6 router rip config['RIP']['process_name'] \n")
                    file.write("redistribute connected\n")
                    file.write("exit")
                    for interface in config['interfaces']:
                        file.write(f" interface {interface['interfaceName']}\n")
                        file.write (f"ipv6 rip enable")
                    

                if 'OSPF' in config:
                    ospf_config = config['OSPF']
                    file.write("ipv6 router ospf 1\n")
                    file.write(f"router-id {ospf_config['routeurId']}\n")
                    file.write("exit")
                    for interface in config['interfaces']:
                        area_id = ospf_config['area']
                        file.write(f" ipv6 ospf 1 area {area_id}\n")
                        file.write("exit")
                    file.write("\n")


                if 'iBGP' and 'RIP' in config:
                    file.write("ipv6 router rip  config['RIP']['process_name'] \n")
                    file.write(f"redistribute bgp {json_data[AS]['autonomousSystem']} include-connected \n")
                    file.write("exit\n")

                    file.write(f"router bgp {json_data[AS]['autonomousSystem']}\n")
                    file.write("address-family ipv6\n")
                    file.write(f"redistribute rip config['RIP']['process_name']\n")
                    file.write("exit\n")                    

                if 'iBGP' and 'OSPF' in config:
                    file.write("ipv6 router ospf 1 \n")
                    file.write(f"redistribute bgp {json_data[AS]['autonomousSystem']} include-connected \n")
                    file.write("exit\n")

                    file.write(f"router bgp {json_data[AS]['autonomousSystem']}\n")
                    file.write("address-family ipv6\n")
                    file.write(f"redistribute ospf 1 match internal external 1 external 2\n")
                    file.write("exit-address-family\n")
                    file.write("exit\n")   

                
                if 'iBGP' in config:
                    asn = json_data[AS]['autonomousSystem']
                    file.write(f"router bgp {asn}\n")
                    file.write(" bgp log-neighbor-changes\n")
                    for peer in config['iBGP']['peers']:
                        file.write(f" neighbor {peer} remote-as {asn}\n")
                        file.write("address-family ipv6 unicast\n")
                        file.write("neighbor {peer} activate\n")
                    file.write("\n")

                if 'eBGP' in config:
                    asn_d = json_data[AS]['autonomousSystem']
                    file.write(f"router bgp {asn_d}\n")
                    for voisin in config["eBGP"]["neighbor"]:
                        asn_a = voisin["remoteAsn"]
                        neighbor = voisin["ipAddress"]
                        file.write(f" neighbor {neighbor} remote-as {asn_a}\n")
                    file.write("\n")

                file.write("!\n")

# Example usage
json_file = 
output_directory = 

with open(json_file, 'r') as file:
    data = json.load(file)

generate_config(data, output_directory)

