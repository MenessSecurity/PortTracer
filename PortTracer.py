import scapy.all as scapy
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import csv
from pyvis.network import Network

def parse_pcap(pcap_file):
    packets = scapy.rdpcap(pcap_file)
    graph_data = []
    seen_connections = set()  # Speichert bereits erfasste Verbindungen

    for packet in packets:
        if packet.haslayer(scapy.IP):  
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst

            if packet.haslayer(scapy.TCP):
                src_port = packet[scapy.TCP].sport
                dst_port = packet[scapy.TCP].dport
                protocol = "TCP"
            elif packet.haslayer(scapy.UDP):
                src_port = packet[scapy.UDP].sport
                dst_port = packet[scapy.UDP].dport
                protocol = "UDP"
            else:
                continue  

            # Prüfen, ob es eine Antwortverbindung ist (gleiche IPs, aber vertauschte Ports)
            if (dst_ip, src_ip, src_port, dst_port, protocol) in seen_connections:
                continue  # Antwortpaket ignorieren

            # Speichern der neuen Verbindung
            seen_connections.add((src_ip, dst_ip, dst_port, src_port, protocol))
            graph_data.append((src_ip, dst_ip, dst_port, protocol))

    return graph_data


def create_graph(graph_data):
    G = nx.DiGraph()  # Direktionaler Graph

    edge_labels = {}  # Speichert die Ports pro Verbindung

    for src, dst, port, protocol in graph_data:
        key = (src, dst)
        if key in edge_labels:
            # Falls die Verbindung schon existiert, neuen Port hinzufügen
            if f"{protocol}/{port}" not in edge_labels[key]:
                edge_labels[key].append(f"{protocol}/{port}")
        else:
            # Neue Verbindung erstellen
            edge_labels[key] = [f"{protocol}/{port}"]

    # Erstelle Kanten mit zusammengefassten Labels
    for (src, dst), ports in edge_labels.items():
        G.add_edge(src, dst, label=", ".join(ports))

    return G

def draw_static_graph(G):
    """ Erstellt ein statisches PNG-Bild des Netzwerkgraphen """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1.0, scale=5.0, seed=42)                    # Automatische Anordnung der Knoten und Erhöhung des Abstandsfaktors

    # Dynamische Knotengröße basierend auf der IP-Länge
    max_text_length = max(len(node) for node in G.nodes())                  # Längste IP Adresse ermitteln
    base_node_size = 2000                                                   # Basisgröße
    node_size = base_node_size + (max_text_length * 500)                    # Skaliert mit Textlänge

    # Zeichne Knoten und Kanten
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=node_size, font_size=10, font_weight="bold")

    # Füge Labels für die Verbindungen (Ports) hinzu
    edge_labels = {(src, dst): data['label'] for src, dst, data in G.edges(data=True)}

    # Automatische Textverschiebung für bessere Sichtbarkeit
    edge_label_pos = {k: (v[0], v[1] + 0.05) for k, v in pos.items()}    

    nx.draw_networkx_edge_labels(G, edge_label_pos, edge_labels=edge_labels, font_color="red", font_size=9)

    plt.title("Netzwerkkommunikation aus PCAP")
    plt.savefig("network_graph.png", dpi=600, bbox_inches="tight")
    print("✅ Statisches Netzwerkdiagramm gespeichert als 'network_graph.png'")

def draw_interactive_graph(G):
    """ Erstellt eine interaktive HTML-Version des Graphen """
    net = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=True)

    for node in G.nodes():
        net.add_node(node, label=node, title=node, color="lightblue")

    for src, dst, data in G.edges(data=True):
        net.add_edge(src, dst, title=data["label"], label=data["label"], color="gray")

    net.repulsion(node_distance=200, spring_length=200)
    net.save_graph("network_graph.html")
    print("✅ Interaktives Netzwerkdiagramm gespeichert als 'network_graph.html'")

def export_to_csv(graph_data, filename="network_connections.csv"):
    # Öffne die Datei im Schreibmodus
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Header für CSV
        writer.writerow(["SRC", "DST", "Zielport"])
        
        # Schreibe jede Verbindung (SRC, DST, Port) in eine Zeile
        for src, dst, port, protocol in graph_data:
            writer.writerow([src, dst, port])
    
    print(f"CSV-Datei wurde erfolgreich unter {filename} gespeichert.")

def main():
    # Argumente für den Exporttyp und den PCAP-Dateinamen
    parser = argparse.ArgumentParser(description="Exportiere Netzwerkgraphen in verschiedene Formate.")
    parser.add_argument('pcap_file', help="Pfad zur PCAP-Datei")
    parser.add_argument('--format', choices=['static', 'interactive', 'csv'], default='static',
                        help="Wähle das Ausgabeformat: 'static' für statisches Bild, 'interactive' für interaktive HTML, 'csv' für CSV-Export.")
    args = parser.parse_args()

    # Lese die angegebene PCAP-Datei
    graph_data = parse_pcap(args.pcap_file)
    G = create_graph(graph_data)

    # Format auswählen
    if args.format == 'static':
        draw_static_graph(G)
    elif args.format == 'interactive':
        draw_interactive_graph(G)
    elif args.format == 'csv':
        export_to_csv(graph_data)

if __name__ == "__main__":
    main()