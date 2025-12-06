import networkx as nx
from typing import List, Dict, Optional
from pydantic import BaseModel

class NetworkNode(BaseModel):
    ip: str
    hostname: str
    os: str
    is_critical: bool = False
    tags: List[str] = []

class NetworkGraph:
    """
    The Map of the Battlefield.
    Uses Graph Theory to track connectivity and 'Distance to Target'.
    """
    def __init__(self):
        # A Directed Graph (packets flow from A to B)
        self.graph = nx.DiGraph()
        
    def add_host(self, ip: str, os: str = "Unknown", critical: bool = False):
        """Add a computer to the map."""
        node_data = NetworkNode(ip=ip, hostname=ip, os=os, is_critical=critical)
        # Store the Pydantic object inside the graph node
        self.graph.add_node(ip, data=node_data)
        
    def add_connection(self, source_ip: str, dest_ip: str, port: int):
        """Add a wire between two computers."""
        self.graph.add_edge(source_ip, dest_ip, port=port)

    def get_critical_assets(self) -> List[str]:
        """Return IPs of all Critical Assets (High Value Targets)."""
        return [n for n, attr in self.graph.nodes(data=True) if attr['data'].is_critical]

    def shortest_path_to_critical(self, start_ip: str) -> Dict[str, List[str]]:
        """
        Use Dijkstra's Algorithm to find the fastest way to the Crown Jewels.
        """
        paths = {}
        targets = self.get_critical_assets()
        
        for target in targets:
            try:
                # Calculate shortest path in the graph
                path = nx.shortest_path(self.graph, source=start_ip, target=target)
                paths[target] = path
            except nx.NetworkXNoPath:
                pass # No physical route exists
                
        return paths

    def export_topology(self) -> Dict:
        """Export for the UI Dashboard."""
        return nx.node_link_data(self.graph)