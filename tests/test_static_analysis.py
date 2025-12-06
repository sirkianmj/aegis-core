from aegis.core.analysis.static import StaticAnalyzer
import os

def test_sink_identification():
    print("=== SPRINT 7: STATIC SINK IDENTIFICATION (COMPLIANCE CHECK) ===")
    
    # We use the overflow target because it uses 'read' (a sink)
    binary_path = "./targets/overflow_app"
    
    if not os.path.exists(binary_path):
        print("Binary missing.")
        return

    analyzer = StaticAnalyzer(binary_path)
    sinks = analyzer.identify_sinks()
    
    # Verification
    sink_names = [s['name'] for s in sinks]
    
    if "read" in sink_names:
        print("\n[SUCCESS] Static Analyzer found 'read' function.")
        print("    This satisfies the 'Dangerous Sink Identification' requirement.")
    else:
        print("\n[FAILURE] Static Analyzer missed the sink.")

if __name__ == "__main__":
    test_sink_identification()