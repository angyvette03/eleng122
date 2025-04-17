from link import Link
from stats import PacketTracker

class Node:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.links = {}

    def add_link(self, other_node, bandwidth):
        link = Link(self.env, bandwidth)
        self.links[other_node] = link

    def send_packet(self, packet, next_hop, tracker=None):
        # print(f"{self.name} sending packet to {next_hop.name} at {self.env.now}")
        link = self.links[next_hop]
        
        # If this is the final destination, record the packet completion
        if packet.dest == next_hop.name and tracker is not None:
            def packet_done(event, pkt=packet):
                pkt.end_time = self.env.now
                transit_time = pkt.end_time - pkt.creation_time
                tracker.record_packet(pkt, transit_time)
            
            transmit_process = self.env.process(link.transmit(packet))
            transmit_process.callbacks.append(packet_done)
        else:
            self.env.process(link.transmit(packet))
            
        yield self.env.timeout(0)  # Simulate sending the packet
