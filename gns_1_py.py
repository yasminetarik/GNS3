"""
Created on Wed Jan  3 16:47:07 2024

@author: HP
"""

import json

def generate_config(json_data, output_dir):
    
    for AS in json_data.keys(): 
        
        for router, config in json_data[AS]['routers'].items():
            
            with open(f"{output_dir}/{router}_config.cfg", 'w') as file:
                file.write(f"! Configuration for {router}\n")
                file.write(f"hostname {router}\n\n")
                file.write("ipv6 unicast-routing \n")

                for interface in config['interfaces']:
                    
                    file.write(f"interface {interface['interfaceName']}\n")
                    file.write(f" ipv6 address {interface['ipAddress']}\n")
                    file.write(" no shutdown\n\n")
                    if 'RIP' in config:
                        file.write (f" ipv6 rip {config['RIP']['process_name']} enable \n")

                if 'RIP' in config:
    
                    file.write(f"ipv6 router rip {config['RIP']['process_name']} \n")
                    file.write(" redistribute connected\n")
                    file.write("\n")
                    #file.write("exit")
                    if 'OSPF' in config:
                        ospf_config = config['OSPF']
                        
                        area_id = ospf_config['area']
                        file.write(f" ipv6 ospf 1 area {area_id}\n")
                        file.write("\n")
                    
                        #file.write(f" ipv6 ospf cost {interface['ospfCost']} \n")
                    

                if 'OSPF' in config:
                    ospf_config = config['OSPF']
                    file.write("ipv6 router ospf 1\n")
                    file.write(f" router-id {ospf_config['routeurId']}\n")
                    file.write(" log-adjacency-changes \n")
                    if 'iBGP' in config:
                        asn = json_data[AS]['autonomousSystem']
                        file.write(f" redistribute bgp {asn} include-connected \n")
                        #file.write("exit")
                    
                    #file.write("exit\n")

                if 'iBGP' in config:
                    asn = json_data[AS]['autonomousSystem']
                    bgp_id=config['iBGP']['routeurId']
                    file.write(f"router bgp {asn}\n")
                    file.write(" bgp log-neighbor-changes\n")
                    file.write(f" bgp router-id {bgp_id} \n") 
                    
                    for peer in config['iBGP']['peers']:
                        file.write(f" neighbor {peer} remote-as {asn}\n")

                    if 'eBGP' in config:
                        asn_d = json_data[AS]['autonomousSystem']
                        conf_ebgp = config['eBGP']

                        #file.write(f"router bgp {asn_d}\n")

                        for neighbor in conf_ebgp["neighbor"]:
                            
                            asn_a = neighbor[1]
                            neighbor_ip = neighbor[0]
                            file.write(f" neighbor {neighbor_ip} remote-as {asn_a}\n")
                    file.write(" no auto-summary \n")


                    
                    file.write(" address-family ipv6 unicast\n")
                    for peer in config['iBGP']['peers']:
                        file.write(f" neighbor {peer} activate\n")
                        #file.write(f"neighbor {peer} send-community both")
                        #file.write("exit-address-family\n")
                    #file.write("no auto-summary")
                    #file.write("exit\n")

                    """if 'RIP' in config:
                        file.write(f"router bgp {asn}\n")
                        file.write(" address-family ipv6\n")
                        file.write(f" redistribute rip {config['RIP']['process_name']}\n")
                        file.write("exit-address-family\n")
                        file.write("exit\n")"""

                    if 'OSPF' in config:
                        #file.write(f"router bgp {asn}\n")
                        #file.write(" address-family ipv6 unicast\n")
                        file.write(" redistribute ospf 1 match internal external 1 external 2\n")
                        file.write("exit-address-family\n")
                        #file.write("exit\n")


                    file.write("\n")



       

# Example usage
json_file = "corrected_test_1.json"
output_directory = "/mnt/c/Users/HP/Desktop/Cours/3_TC/GNS"

with open(json_file, 'r') as file:
    data = json.load(file)

generate_config(data, output_directory)

