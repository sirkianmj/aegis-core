from aegis.core.network.graph import NetworkGraph

def test_pathfinding():
    print("=== SPRINT 2: GRAPH THEORY TEST ===")
    
    # 1. Initialize Map
    net = NetworkGraph()
    
    # 2. Add Hosts (Nodes)
    # Attacker -> JumpBox -> Database (Critical)
    net.add_host("1.1.1.1", os="Kali", critical=False)     # Attacker
    net.add_host("192.168.1.5", os="Ubuntu", critical=False) # Web Server
    net.add_host("10.0.0.99", os="Windows", critical=True)   # The Target
    
    # 3. Add Connectivity (Edges)
    # Attacker can see Web Server (Port 80)
    net.add_connection("1.1.1.1", "192.168.1.5", port=80)
    
    # Web Server can see Database (Port 3306) - "Pivoting"
    net.add_connection("192.168.1.5", "10.0.0.99", port=3306)
    
    # 4. Ask AEGIS: "How do I get to the Critical Asset?"
    routes = net.shortest_path_to_critical("1.1.1.1")
    
    target_ip = "10.0.0.99"
    if target_ip in routes:
        print(f"[SUCCESS] Path Found: {routes[target_ip]}")
        print("    Hop 1: Attacker -> Web Server")
        print("    Hop 2: Web Server -> Database")
    else:
        print("[FAILURE] No path found.")

if __name__ == "__main__":
    test_pathfinding()