"""
OPC UA Data Logger for Pfeiffer HiCube 80 Neo
--------------------------------------------
This script connects to an OPC UA server, allows browsing of available nodes,
retrieves pressure data, and logs it to a text file every second.

Author: Sebastian Pucher
Date: 2025-02-18
Version: 1.0

Usage:
- Run the script to continuously log pressure values every second.
- Press `CTRL+C` to stop.
- Uncomment `browse_nodes(SERVER_URL)` to explore available nodes before logging.

Dependencies:
- opcua (pip install opcua)
- Python 3.x

"""

import time
from opcua import Client
from datetime import datetime

def connect_to_server(server_url):
    """
    Establishes a connection to the OPC UA server.

    Parameters:
        server_url (str): The OPC UA server URL.

    Returns:
        Client or None: An instance of the OPC UA client if successful, otherwise None.
    """
    client = Client(server_url)
    try:
        client.connect()
        print(f"Connected to OPC UA server at {server_url}")
        return client
    except Exception as e:
        print(f"Error connecting to OPC UA server: {e}")
        return None

def browse_nodes(client):
    """
    Browses and lists all available nodes in the OPC UA server.

    Parameters:
        client (Client): The connected OPC UA client.
    """
    try:
        root = client.get_root_node()
        print(f"Root Node: {root}")

        objects = client.get_objects_node()
        print("Browsing Objects...")

        for obj in objects.get_children():
            print(f"Node: {obj}, Browse Name: {obj.get_browse_name()}")

            for child in obj.get_children():
                print(f"   ↳ Child Node: {child}, Browse Name: {child.get_browse_name()}")

    except Exception as e:
        print(f"Error browsing nodes: {e}")

def read_pressure(client, node_id):
    """
    Reads the pressure value from the OPC UA server.

    Parameters:
        client (Client): The connected OPC UA client.
        node_id (str): The node ID for the pressure value.

    Returns:
        float or None: The pressure value, or None if reading fails.
    """
    try:
        pressure_node = client.get_node(node_id)
        return pressure_node.get_value()
    except Exception as e:
        print(f"Error reading pressure data: {e}")
        return None

def get_current_timestamp():
    """
    Retrieves the current date and time in a formatted string.

    Returns:
        str: The current timestamp in "YYYY-MM-DD HH:MM:SS" format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_data(log_file, timestamp, pressure):
    """
    Logs the timestamp and pressure value to a text file.

    Parameters:
        log_file (str): The file path for logging.
        timestamp (str): The current timestamp.
        pressure (float): The measured pressure value.
    """
    try:
        with open(log_file, "a") as file:
            log_entry = f"{timestamp}, {pressure} mbar\n"
            file.write(log_entry)
            print(f"Logged: {log_entry.strip()}")
    except Exception as e:
        print(f"Error writing to log file: {e}")

if __name__ == "__main__":
    """
    Connects to the OPC UA server and continuously logs pressure data.
    Runs indefinitely until the user stops the script manually (CTRL+C).
    """
    # Server Configuration
    SERVER_URL = "opc.tcp://10.0.5.76:4840"    # OPC UA Server Address
    PRESSURE_NODE_ID = "ns=1;s=G1_pressure"    # Node ID for pressure measurement
    LOG_FILE = "pressure_log.txt"              # Output file for logging
    LOG_INTERVAL = 10                            # Interval (seconds) between measurements

    # Connect to OPC UA Server
    client = connect_to_server(SERVER_URL)
    if client is None:
        exit()  # Exit if connection fails

    # Browse nodes first (Optional: Uncomment to run before logging)
    # browse_nodes(client)

    try:
        while True:
            # Get current pressure reading
            pressure = read_pressure(client, PRESSURE_NODE_ID)
            if pressure is not None:
                timestamp = get_current_timestamp()
                log_data(LOG_FILE, timestamp, pressure)

            # Wait before the next measurement
            time.sleep(LOG_INTERVAL)

    except KeyboardInterrupt:
        print("\nUser stopped the script. Exiting...")

    finally:
        client.disconnect()
        print("Disconnected from OPC UA server.")

