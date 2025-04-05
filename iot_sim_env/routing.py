import random
from packet import Packet 

def traffic_generator(env, src_node, dest_node, size_choice, tracker):
    while True:
        # Generate packet with appropriate size
        if size_choice == 0:  
            packet_size = random.randint(10, 100)
        elif size_choice == 1:  
            packet_size = random.randint(101, 500)
        else:  
            packet_size = random.randint(501, 1500)
            
        packet = Packet(packet_size, src_node.name, dest_node.name)
        packet.creation_time = env.now  # Set creation time
        
        # Send packet
        env.process(src_node.send_packet(packet, next_hop=dest_node, tracker=tracker))
        yield env.timeout(random.expovariate(1))