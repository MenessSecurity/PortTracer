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

Install the required packages:


```bash
pip install scapy networkx matplotlib pyvis
```



Start the script with a PCAP file:

```bash
python PortTracer.py <pcap> --format <static | interactive | csv> 
```


## Authors

- [@MenessSecurity](https://github.com/MenessSecurity)
