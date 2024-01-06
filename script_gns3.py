# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:47:07 2024

@author: HP
"""

import json



def generate_config(json_data):
    #make it loop through all the ASs
    for AS in json_data.keys(): 
    # Loop through each router in the JSON data
        for router, config in json_data[AS]['routers'].items():
            print(f"! Configuration for {router}")
            print(f"hostname {router}\n")

        
            for interface in config['interfaces']:
                print(f"interface {interface['interfaceName']}")
                print(f" ip address {interface['ipAddress']} {interface['subnetMask']}")
                print("no shutdown")

        
            if 'RIP' in config:
                print("router rip")
                print(" version 2")
                for network in config['RIP']['networks']:
                    print(f" network {network}")
                    print("\n")
                print("no auto-summary")
                    
                    
            if 'OSPF' in config:
                ospf_config= config['OSPF']
                print("router ospf 1")
                for network in ospf_config['networks']:
                    nw= network['network']
                    mask= network['wildcardMask']
                    area_id= network['area']
                    
                    print(f"network {nw} {mask} area {area_id}")
                ##à faire après la 2eme partie du intent file

        
            if 'iBGP' in config:
                asn = json_data[AS]['autonomousSystem']
                print(f"router bgp {asn}")
                print("bgp log-neighbor-changes")
                for peer in config['iBGP']['peers']:
                    print(f" neighbor {peer} remote-as {asn}")
                    
                

         
            if 'eBGP' in config:
                asn_d = json_data[AS]['autonomousSystem']
                print(f"router bgp {asn_d}")
                for voisin in config["eBGP"]["neighbor"]:
                
                    asn_a = voisin["remoteAsn"]
                    neighbor=voisin["ipAddress"]
            
                    print(f"neighbor {neighbor} remote-as {asn_a}")
            

            print("!\n")




with open(json_file, 'r') as file:
    data = json.load(file)


generate_config(data)
