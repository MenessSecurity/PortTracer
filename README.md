# PortTracer

This Python script analyzes a PCAP file and visualizes network communication using Scapy and NetworkX. It extracts source IP, destination IP, and destination ports (TCP/UDP) to generate a graph-based representation of network traffic.
Key Features:

- ✅ Reads and parses PCAP files to identify network connections
- ✅ Extracts source IP, destination IP, protocol, and ports
- ✅ Builds a directed graph using NetworkX
- ✅ Labels edges with protocol and port numbers
- ✅ Displays an interactive visualization with Matplotlib
- ✅ Exports a summary of all source and destination addresses including destination port via CSV 

This tool helps analyze network traffic, detect communication patterns, and support firewall rule creation. 🚀
## Roadmap

- Improved image generation
- Weighting of edges according to frequency
- Performance


## Usage/Examples

### Option 1: Directly via Python (global installation)
If you have installed or are installing the required libraries globally on your system, you can simply run the script directly:


Install the required packages:


```bash
pip install scapy networkx matplotlib pyvis
```



Start the script with a PCAP file:

```bash
python PortTracer.py <pcap> --format <static | interactive | csv> 
```

### Option 2: In a virtual environment (recommended)
A virtual environment ensures that the required libraries are only installed for this project and that there are no conflicts with other Python projects. This is how it works:

**Create a virtual environment:**

```bash
python -m venv myenv
```

**Activate the virtual environment:**

Windows:

```bash
myenv\Scripts\activate
```

Mac/Linux:

```bash
source myenv/bin/activate
```

**Install the required packages:**

```bash
pip install scapy networkx matplotlib pyvis
```


**Start the script:**

```bash
python PortTracer.py <pcap> --format <static | interactive | csv> 
```

### Option 3: With Jupyter Notebook
If you want to work interactively and analyse the data step by step, you can also run the script in a Jupyter notebook:

**Install Jupyter Notebook (if not already installed):**

```bash
pip install notebook
```

**Start the Jupyter notebook:**

```bash
jupyter notebook
```

Create a new notebook file and insert the code cells to run the script interactively.
## Authors

- [@MenessSecurity](https://github.com/MenessSecurity)
