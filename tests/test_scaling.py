import time
import networkx as nx
import os
import sys

# Ensure path is correct
sys.path.append(os.getcwd())

from aegis.core.network.graph import NetworkGraph

def test_enterprise_scaling():
    print("=== SPRINT 24: 10,000 NODE SCALING TEST ===")
    
    net = NetworkGraph()
    target_scale = 10000
    
    print(f"[SETUP] Generating synthetic network with {target_scale} nodes...")
    start_gen = time.time()
    
    # 1. Generate massive topology (Barabasi-Albert model simulates real internet)
    # This creates a realistic "Scale-Free" network
    temp_graph = nx.barabasi_albert_graph(target_scale, 3)
    
    # 2. Ingest into AEGIS
    # We do this manually to simulate the overhead of object creation
    for n in temp_graph.nodes():
        is_crit = (n == target_scale - 1) # Last node is critical
        net.add_host(str(n), "Linux", critical=is_crit)
        
    for u, v in temp_graph.edges():
        net.add_connection(str(u), str(v), 80)
        
    duration_gen = time.time() - start_gen
    print(f"    -> Generation complete in {duration_gen:.2f}s")
    
    # 3. Pathfinding Stress Test
    print("[STRESS] Calculating attack path across 10,000 nodes...")
    start_path = time.time()
    
    # Find path from Node 0 to Node 9999
    paths = net.shortest_path_to_critical("0")
    
    duration_path = time.time() - start_path
    
    # 4. Metrics
    target_key = str(target_scale - 1)
    if target_key in paths:
        path_len = len(paths[target_key])
        print(f"\n[SUCCESS] Path found! Length: {path_len} hops.")
        print(f"    -> Calculation Time: {duration_path:.4f}s")
        
        # Verify O(N) performance constraint
        if duration_path < 2.0:
            print("[VERDICT] PASS. System performs under < 2s latency at scale.")
        else:
            print("[VERDICT] WARN. Performance lagging.")
    else:
        print("[FAIL] Pathfinding timed out or failed.")

if __name__ == "__main__":
    test_enterprise_scaling()
