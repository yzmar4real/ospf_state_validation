from pyats.log.utils import banner
import logging
import sys
import requests
import pandas as pd
from tabulate import tabulate

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger()

def get_ospf_state(Device_IP,Username,Passwd):

    url = f"https://{Device_IP}/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state"

    print(url)

    payload = {}
    ospf_headers = {
    'Content-Type': 'application/yang-data+json'
    }
    # Send GET request
    response = requests.get(url, headers=ospf_headers, auth=(Username, Passwd), data=payload, verify=False)
    
    ospf_info_list = []

    # Check if the request was successful
    if response.status_code == 200:
        neighbors_data = response.json()['Cisco-IOS-XE-ospf-oper:ospf-state']['ospf-instance']
        for instance in neighbors_data:
            ospf_info = {}
            
            ospf_info["Router-ID"] = instance["router-id"]
            ospf_info["OSPF Process ID"] = instance["process-id"]
            ospf_info["Areas"] = []

            for area in instance["ospf-area"]:
                area_info = {}
                area_info["Area-ID"] = area["area-id"]
                area_info["Interfaces"] = []

                for iface in area["ospf-interface"]:
                    interface_info = {}

                    interface_info["Name"] = iface["name"]
                    interface_info["Network Type"] = iface["network-type"]
                    interface_info["Cost"] = iface["cost"]
                    interface_info["Enabled"] = iface["enable"]
                    interface_info["Authentication"] = list(iface["authentication"].keys())[0]
                    interface_info["Neighbors"] = []

                    try:
                        for neighbor in iface["ospf-neighbor"]:
                            neighbor_info = {}
                            neighbor_info["Neighbor ID"] = neighbor["neighbor-id"]
                            neighbor_info["Address"] = neighbor["address"]
                            neighbor_info["State"] = neighbor["state"]
                            interface_info["Neighbors"].append(neighbor_info)
                    except Exception as e:
                        print('No Neighbors Detected')

                    area_info["Interfaces"].append(interface_info)
                
                ospf_info["Areas"].append(area_info)
            
            ospf_info_list.append(ospf_info)
        
        # print(ospf_info_list)

        return ospf_info_list
    else:
        print(f"Failed to retrieve OSPF neighbors. Status code: {response.status_code}")
        print(response.text)

def arrange_ospf(ospf_state):

    flattened_data = []

    for item in ospf_state:
        router_id = item['Router-ID']
        ospf_id = item['OSPF Process ID']
            
        for area in item['Areas']:
            area_id = area['Area-ID']
                
            for interface in area['Interfaces']:
                interface_name = interface['Name']
                network_type = interface['Network Type']
                cost = interface['Cost']
                enabled = interface['Enabled']
                authentication = interface['Authentication']
                    
                for neighbor in interface['Neighbors']:
                    neighbor_id = neighbor['Neighbor ID']
                    address = neighbor['Address']
                    state = neighbor['State']
                        
                    flattened_data.append([
                        router_id, ospf_id, area_id, interface_name, network_type, cost, enabled, authentication, neighbor_id, address, state
                    ])

    # Convert to DataFrame
    df = pd.DataFrame(flattened_data, columns=[
        'Router-ID', 'OSPF Process ID', 'Area-ID', 'Interface Name', 'Network Type', 'Cost', 'Enabled', 'Authentication', 'Neighbor ID', 'Address', 'State'
    ])

    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
def ospf_failure(ospf_state_info):

    ospf_state_failure = ['DOWN', 'EXSTART', 'INIT', 'EXCHANGE', '2-WAY', 'LOADING']

    for instance in ospf_state_info:
        data = []
        for area in instance['Areas']:
            for interface in area['Interfaces']:
                ospf_intf_name = interface['Name']
                for neighbor in interface['Neighbors']:
                    ospf_id = neighbor['Neighbor ID']
                    ospf_address = neighbor['Address']
                    ospf_state = neighbor['State']
            
                    for failure_word in ospf_state_failure:
                        # print(failure_word,ospf_state)
                        if failure_word in ospf_state:
                            faulty_neighbor = {'Reference Device': ospf_intf_name,
                                               'Failure Neighbor': ospf_address, 
                                               'Faulty Interface': neighbor, 
                                               'Faulty State': ospf_state}
                            data.append(faulty_neighbor)
                        else:
                            continue
                            # print('No OSPF failures found')
                                               
    return (data)

