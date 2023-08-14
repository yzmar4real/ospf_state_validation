# Importing necessary libraries
import sys
import os
import logging
import getpass
from pyats.log.utils import banner
from functions.ospf import get_ospf_state, ospf_failure, arrange_ospf

# Configuring logging settings to display logs to stdout with the specified format
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger()

# Displaying an informational banner to indicate the start of the OSPF Neighbor State Assurance API
log.info(banner("LOADING OSPF NEIGHBOR STATE ASSURANCE API"))

# Prompting the user for device IP, username, and password for the device they wish to check
Device_IP = input("Please enter your Device IP Address: ")
Username = input("Please enter your username: ")
Passwd = getpass.getpass("Please enter your password: ")  # getpass is used to securely input password without displaying it

# Defining the main function that checks OSPF state
def ospf_checker():
    # Fetching the OSPF state from the device
    ospf_state = get_ospf_state(Device_IP, Username, Passwd)

    # Arranging or processing the fetched OSPF state
    arrange_ospf(ospf_state)

    # Checking if there are any OSPF failures and handling them
    failure_check = ospf_failure(ospf_state)

# This conditional ensures the script only runs ospf_checker when executed directly and not when imported
if __name__ == "__main__":
    try:
        ospf_checker()
    except:
        # Logging any connection failures to the device
        log.info(f"Failed to connect to {Device_IP}")
