import simpy
from node import Node
from routing import traffic_generator
from stats import PacketTracker

def run_simulation(strategy, tracker):
    env = simpy.Environment()

    # Create nodes
    node_A = Node(env, "A")
    node_B = Node(env, "B")
    node_C = Node(env, "C")

    # Define the network topology
    # Current topology: nodeA - nodeB - node C
    node_A.add_link(node_B, bandwidth=1_000_000)  # 1 Mbps
    node_B.add_link(node_C, bandwidth=1_000_000)  # 1 Mbps

    # Start traffic generation for each strategy
    env.process(traffic_generator(env, node_A, node_B, size_choice=0, tracker=tracker, strategy=strategy, threshold=100, aggregation_interval=5))
    env.process(traffic_generator(env, node_B, node_C, size_choice=1, tracker=tracker, strategy=strategy, threshold=100, aggregation_interval=5))

    # Run the simulation, 10 is the duration in seconds of simulated activity
    env.run(until=10)

    # Return the final statistics
    final_stats = tracker.get_statistics()
    size_stats = tracker.get_size_statistics()
    
    return final_stats, size_stats

def main():
    strategies = ['periodic', 'threshold', 'temporal_aggregation']
    
    for strategy in strategies:
        print(f"\n=== Running Simulation with {strategy.capitalize()} Transmission ===")
        
        # Initialize the packet tracker for each run
        tracker = PacketTracker()
        
        # Run the simulation for the current strategy
        final_stats, size_stats = run_simulation(strategy, tracker)
        
        # Print the results
        print("\n=== FINAL NETWORK STATISTICS ===")
        print(f"Strategy: {strategy.capitalize()}")
        print(f"Total packets: {final_stats['total_packets']}")
        print(f"Total bytes transmitted: {final_stats['total_bytes']}")
        print(f"Average packet size: {final_stats['avg_packet_size']:.2f} bytes")
        print(f"Average transit time: {final_stats['avg_transit_time']:.6f} seconds")
        print(f"Network throughput: {final_stats['packets_per_second']:.2f} packets/second")
        
        print(f"\nSize distribution:")
        print(f"  Small (<100B): {size_stats['size_distribution']['small']}")
        print(f"  Medium (100-500B): {size_stats['size_distribution']['medium']}")
        print(f"  Large (>500B): {size_stats['size_distribution']['large']}")
        print(f"  Size Percentiles: {size_stats['size_percentiles']}")

if __name__ == "__main__":
    main()
