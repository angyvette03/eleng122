# copied from some network simulation tools website
import simpy
import random

class Packet:
    def __init__(self, size, src, dest):
        self.size = size
        self.src = src
        self.dest = dest

class Link:
    def __init__(self, env, bandwidth):
        self.env = env
        self.bandwidth = bandwidth  # Bandwidth in bits per second

    def transmit(self, packet):
        transmission_time = packet.size * 8 / self.bandwidth
        yield self.env.timeout(transmission_time)
        print(f"Packet transmitted from {packet.src} to {packet.dest} in {transmission_time:.2f} seconds")

class Node:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.links = {}

    def add_link(self, other_node, bandwidth):
        link = Link(self.env, bandwidth)
        self.links[other_node] = link

    def send_packet(self, packet, next_hop):
        print(f"{self.name} sending packet to {next_hop.name} at {self.env.now}")
        link = self.links[next_hop]
        self.env.process(link.transmit(packet))
        yield self.env.timeout(0)  # Simulate sending the packet

def traffic_generator(env, src_node, dest_node):
    while True:
        packet_size = random.randint(1000, 5000)  # bytes
        packet = Packet(packet_size, src_node.name, dest_node.name)
        env.process(src_node.send_packet(packet, next_hop=dest_node))
        yield env.timeout(random.expovariate(1))  # Random inter-arrival

# ======================
# Set up the simulation
# ======================
env = simpy.Environment()

# Create nodes
node_A = Node(env, "A")
node_B = Node(env, "B")
node_C = Node(env, "C")

# Define the network topology
node_A.add_link(node_B, bandwidth=1_000_000)  # 1 Mbps
node_B.add_link(node_C, bandwidth=1_000_000)  # 1 Mbps

# Start traffic generation
env.process(traffic_generator(env, node_A, node_B))
env.process(traffic_generator(env, node_B, node_C))

# Run the simulation
env.run(until=10)
