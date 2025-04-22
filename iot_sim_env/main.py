import simpy
from node import Node
from routing import traffic_generator
from stats import PacketTracker
import pandas as pd
import os

def run_simulation(strategy, tracker, lambda_val):
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
    env.process(traffic_generator(env, node_A, node_B, size_choice=0, tracker=tracker, strategy=strategy, threshold=100, aggregation_interval=5, lambda_val=lambda_val))
    # env.process(traffic_generator(env, node_B, node_C, size_choice=1, tracker=tracker, strategy=strategy, threshold=100, aggregation_interval=5))
    # env.process(traffic_generator(env, node_B, node_C, size_choice=2, tracker=tracker, strategy=strategy, threshold=100, aggregation_interval=5))

    # Run the simulation, 10 is the duration in seconds of simulated activity
    env.run(until=100)

    # Return the final statistics
    final_stats = tracker.get_statistics()
    size_stats = tracker.get_size_statistics()
    
    return final_stats, size_stats

def main():
    results = []
    strategies = ['periodic', 'threshold', 'temporal_aggregation']
    def frange(start, stop, step):
        while start <= stop:
            yield round(start, 2)
            start += step

    lambdas = list(frange(0.1, 10.0, 0.1))

    for strategy in strategies:
        for lambda_value in lambdas:
            print(f"\n=== Running Simulation with {strategy.capitalize()} Transmission and Frequency = {lambda_value} ===")
            
            # Initialize the packet tracker for each run
            tracker = PacketTracker()
            
            # Run the simulation for the current strategy
            final_stats, size_stats = run_simulation(strategy, tracker, lambda_value)
            
            # Print the results
            print("\n=== FINAL NETWORK STATISTICS ===")
            print(f"Strategy: {strategy.capitalize()}")
            print(f"Total packets sent: {final_stats['total_packets_sent']}")
            print(f"Total packets generated: {final_stats['total_packets_generated']}")
            print(f"Total bytes transmitted: {final_stats['total_bytes']}")
            print(f"Average packet size: {final_stats['avg_packet_size']:.2f} bytes")
            print(f"Average transit time: {final_stats['avg_transit_time']:.6f} seconds")
            print(f"Network throughput: {final_stats['packets_per_second']:.2f} packets/second")
            
            # print(f"\nSize distribution:")
            # print(f"  Small (<100B): {size_stats['size_distribution']['small']}")
            # print(f"  Medium (100-500B): {size_stats['size_distribution']['medium']}")
            # print(f"  Large (>500B): {size_stats['size_distribution']['large']}")
            # print(f"  Size Percentiles: {size_stats['size_percentiles']}")
            
            results.append({
                "strategy": strategy,
                "lambda": lambda_value,
                "total_packets_sent": final_stats["total_packets_sent"],
                "total_packets_generated": final_stats["total_packets_generated"],
                "total_bytes": final_stats["total_bytes"],
                "avg_packet_size": final_stats["avg_packet_size"],
                "packets_per_second": final_stats["packets_per_second"],
                "avg_transit_time": final_stats["avg_transit_time"]
            })
            # print(results)
    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()