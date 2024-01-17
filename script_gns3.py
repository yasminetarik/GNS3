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
                        file.write(f"interface {interface['interfaceName']}\n")
                        area_id = ospf_config['area']
                        file.write(f" ipv6 ospf 1 area {area_id}\n")
                    file.write("exit\n")

                if 'iBGP' in config:
                    asn = json_data[AS]['autonomousSystem']
                    file.write(f"router bgp {asn}\n")
                    file.write(" bgp log-neighbor-changes\n")
                    
                    for peer in config['iBGP']['peers']:
                        file.write(f" neighbor {peer} remote-as {asn}\n")
                        
                        file.write(" address-family ipv6 unicast\n")
                        file.write(f" neighbor {peer} activate\n")
                        file.write(f"neighbor {peer} send-community both")
                        file.write("exit-address-family\n")
                    file.write("exit\n")

                    if 'RIP' in config:
                        file.write(f"router bgp {asn}\n")
                        file.write(" address-family ipv6\n")
                        file.write(f" redistribute rip {config['RIP']['process_name']}\n")
                        file.write("exit-address-family\n")
                        file.write("exit\n")

                    if 'OSPF' in config:
                        file.write(f"router bgp {asn}\n")
                        file.write(" address-family ipv6 unicast\n")
                        file.write(" redistribute ospf 1 match internal external 1 external 2\n")
                        file.write("exit-address-family\n")
                        file.write("exit\n")


                if 'eBGP' in config:
                    asn_d = json_data[AS]['autonomousSystem']
                    conf_ebgp = config['eBGP']

                    file.write(f"router bgp {asn_d}\n")

                    for neighbor in conf_ebgp["neighbors"]:
                        route = neighbor["route_map"]
                        asn_a = neighbor["remoteAsn"]
                        neighbor_ip = neighbor["ipAddress"]
                        set_community = route["set_community"] 
                        relationship= neighbor.get("community", "peer")

                        if relationship == 'customer':
                            local_pref = 150
                        elif relationship == 'peer':
                            local_pref = 100
                        elif relationship == 'provider':
                            local_pref = 50
                        else:
                            local_pref = 100
                        
                        file.write(f" neighbor {neighbor_ip} remote-as {asn_a}\n")

                        file.write(f"route-map {route['community']} {route['action']} {route['sequence']}\n")
                        
                        file.write(f" set community {set_community}\n")
                        file.write(f"set local-preference {local_pref}\n")
                        file.write("exit\n")

                    file.write(" address-family ipv6 unicast\n")
                    for neighbor in conf_ebgp["neighbors"]:
                        route = neighbor["route_map"]
                        file.write(f" neighbor {neighbor['ipAddress']} route-map {route['community']} in\n")
                        
                    file.write("exit-address-family\n")
                    file.write("exit\n")
                file.write("\n")


                for neighbor in conf_ebgp["neighbors"]:
                    route = neighbor["route_map"]
                    relationship = route['community']
                    if relationship == 'customer':
                        local_pref = 150
                    elif relationship == 'peer':
                        local_pref = 100
                    elif relationship == 'provider':
                        local_pref = 50
                    else:
                        local_pref = 100 


# Example usage
json_file = 
output_directory = 

with open(json_file, 'r') as file:
    data = json.load(file)

generate_config(data, output_directory)

