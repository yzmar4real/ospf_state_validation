# ospf_state_validation
This repository demonstrates the power of RESTCONF and Python in checking the state of OSPF on a Router and validating that the neighbor adjacency is healthy. 

## Overview

 Python Code that allows Network Engineers to run through their existing infrastructure running IOSXE Software to validate OSPF neighbor adjacency and report if any of the neighbors are not healthy.

## Use Case Description

This use case is particularly helpful in validating network routing information for OSPF adjacencies to ensure full convergence and user stability. 

**Python**

The script is written in python using RESTCONF to interact with the active devices and extract information. 

**Output**: 

The output of the script displays in a table information about the ospf state, and identifies issues with the adjacency if possible. 

## Contacts

*Oluyemi Oshunkoya (yemi_o@outlook.com)

## Solution Components
*Python
*RESTCONF
*CML (You will require live routers to perform these tests on)
*IOS XE Routers

## Prerequisites 

Python3.6 and above

CML or live lab environment

Restconf enabled IOSXE devices.(IOSXE 17.6.1 image was used for this test)

## Toolbox

This tool leverages the power of RESTCONF and programability for Cisco IOS XE devices. It enables you communicate via REST API's to extract relevant information from the network devices(In this case OSPF adjacency).

## Step 1 - Initial Setup - (Assuming you have an active python setup)

1. Clone the repository

git clone https://github.com/yzmar4real/ospf_state_validation.git

2. CD into the directory 

cd ospf_state_validation

3. (Optional) Use the directory as a virtual environment for the project

python3 -m venv . 

4. (Optional) Start the virtual environment and install the requirements for the project

source bin/activate

## Step 2 - Installing the pre-requisites

pip install pyats pandas tabulate

## Step 3 - Executing the Script 

1. Execute the main script from console

python3 Main.py

