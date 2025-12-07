import time
import sys
import os
import statistics

# Add root to path so we can import aegis
sys.path.append(os.getcwd())

try:
    from aegis.core.logic.engine import ReasoningEngine
    from aegis.core.logic.grammar import FactType
    from aegis.core.exploitation.payload_factory import PayloadFactory
except ImportError:
    print("CRITICAL: Run this script from the project root directory.")
    sys.exit(1)

class BenchmarkSuite:
    def __init__(self):
        self.results = {}

    def measure_logic_speed(self):
        print("[BENCH] Measuring Z3 Logic Inference Speed (N=1000)...")
        engine = ReasoningEngine()
        engine.load_rules()
        
        timings = []
        # Warmup
        engine.analyze_feasibility(FactType.CREDENTIAL_FOUND, [FactType.PORT_OPEN])
        
        for _ in range(1000):
            start = time.perf_counter()
            engine.analyze_feasibility(FactType.CREDENTIAL_FOUND, [FactType.PORT_OPEN])
            end = time.perf_counter()
            timings.append((end - start) * 1000) # Convert to ms
        
        avg_ms = statistics.mean(timings)
        p99_ms = statistics.quantiles(timings, n=100)[98] # 99th percentile
        
        print(f"    -> Avg Inference: {avg_ms:.4f} ms")
        print(f"    -> 99th % Latency: {p99_ms:.4f} ms")
        self.results['logic_ms'] = avg_ms

    def measure_payload_gen(self):
        print("[BENCH] Measuring Exploit Generation Speed (N=1000)...")
        factory = PayloadFactory()
        
        timings = []
        for _ in range(1000):
            start = time.perf_counter()
            # Generate a standard overflow payload
            factory.generate_buffer_overflow(72, 0x400000)
            end = time.perf_counter()
            timings.append((end - start) * 1000)
            
        avg_ms = statistics.mean(timings)
        print(f"    -> Avg Generation: {avg_ms:.4f} ms")
        self.results['payload_ms'] = avg_ms

    def run(self):
        print("=== AEGIS PERFORMANCE BENCHMARK ===")
        self.measure_logic_speed()
        self.measure_payload_gen()
        
        # Pass/Fail Criteria (Sub-10ms is the goal for real-time systems)
        if self.results['logic_ms'] < 15.0 and self.results['payload_ms'] < 5.0:
            print("\n[SUCCESS] System meets Real-Time Operational standards.")
        else:
            print("\n[WARN] Performance degradation detected. Optimization needed.")

if __name__ == "__main__":
    b = BenchmarkSuite()
    b.run()