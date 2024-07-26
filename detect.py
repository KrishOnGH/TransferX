import os
import platform
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_arp_table():
    """Retrieve the ARP table."""
    if platform.system().lower() == 'windows':
        command = 'arp -a'
    else:
        command = 'arp -n'
    
    try:
        result = subprocess.check_output(command, shell=True).decode()
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving ARP table: {e}")
        return ""

def parse_arp_table(arp_table):
    """Parse the ARP table to extract IP and MAC addresses."""
    devices = []
    lines = arp_table.split('\n')
    
    for line in lines:
        if platform.system().lower() == 'windows':
            if 'dynamic' in line:
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    mac = parts[1]
                    devices.append((ip, mac))
        else:
            if len(line.split()) >= 2:
                parts = line.split()
                ip = parts[0]
                mac = parts[1]
                devices.append((ip, mac))
    
    return devices

def main():
    arp_table = get_arp_table()
    devices = parse_arp_table(arp_table)
    
    for device in devices:
        ip, mac = device
        logging.info(f"Device IP: {ip}, Device MAC: {mac}")

if __name__ == "__main__":
    main()
