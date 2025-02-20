# OPC UA Data Logging and Visualization for Pfeiffer HiCube 80 Neo

This repository contains a python script for measuring vacuum chamber pressures using a Pfeiffer Vacuum PKR 361 pressure gauge (P\N PT T03 350 010). The gauge is connected to a Pfeiffer Vacuum HiCube 80 Neo pump stand (P\N PM Q102 003 00), which accurately displays the measured pressure values.
The HiCube 80 Neo is connected to the network via Ethernet, allowing remote access to the pressure data. The IP address of the HiCube 80 Neo can be found in its settings. The script communicates with the OPC UA server running on the HiCube 80 Neo to continuously log pressure measurements for further analysis.

This repository contains three key files:
1. **`measure_pressure.py`** - A Python script that connects to an OPC UA server, retrieves pressure data from the Pfeiffer HiCube 80 Neo, and logs it to a text file in real time.
2. **Sample Data (`pressure_log.txt`)** - Pre-generated sample data representing recorded pressure values over time.
3. **Jupyter Notebook (`plot_pressure.ipynb`)** - A visualization tool to load and plot the logged pressure data for analysis.

## Features

- Connects to an OPC UA server
- Reads pressure data from a specified OPC UA node
- Logs data to a text file every second until stopped manually
- Includes a function to browse all available OPC UA nodes to find the correct one
- Jupyter Notebook for easy visualization of the logged data

## Prerequisites

- Python 3.x
- opcua library
- matplotlib and pandas (for the notebook)

## Install Dependencies

```
pip install opcua
```
```
conda install conda-forge::opcua
```

## Usage

### 1. Find the Correct Node (Optional)

Before running the logging script, you can explore available OPC UA nodes by running:


```
browse_nodes(client)
```

This will list all available nodes, helping you identify the correct node for pressure readings.

### 2. Run the Measurement Script

Once the correct node is identified, update the script with the correct node ID and run:

```
python measure_pressure.py
```

The script will log pressure data to pressure_log.txt every second.

### 3. Stop the Script

Press CTRL+C to stop logging. The script will disconnect safely from the OPC UA server.

### 4. Plot the Data using Jupyter Notebook

To visualize the logged pressure data, use the jupyter notebook. This will generate a time-series plot of the recorded pressure values.

## Configuration

Modify the following variables in `measure_pressure.py` to match your setup:

```python
SERVER_URL = "opc.tcp://192.168.1.100:4840"  # OPC UA Server Address (Change IP address, OPC UA standard port is 4840)
PRESSURE_NODE_ID = "ns=1;s=G1_pressure"      # Node ID for pressure measurement
LOG_FILE = "pressure_log.txt"                # Output file for logging
LOG_INTERVAL = 1                             # Interval (seconds) between measurements
```

## Example Log Output

```
2025-02-12 11:28:13, 1.9899999870176543e-09 mbar
2025-02-12 11:28:23, 2.0000000233721948e-09 mbar
2025-02-12 11:29:48, 1.9899999870176543e-09 mbar
2025-02-12 11:29:58, 2.0000000233721948e-09 mbar
2025-02-12 11:30:08, 1.9899999870176543e-09 mbar
2025-02-12 11:30:18, 1.9899999870176543e-09 mbar
2025-02-12 11:30:28, 2.0000000233721948e-09 mbar
```
