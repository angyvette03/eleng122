import random
from packet import Packet 

def traffic_generator(env, src_node, dest_node, size_choice, tracker, strategy="periodic", threshold=100, aggregation_interval=5, lambda_val=1):
    last_sent_time = 0  # Track last sent time for periodic transmission
    last_sent_data = None  # Track the last data value for threshold-based transmission
    accumulated_data = []  # List to accumulate data for temporal aggregation
    aggregation_timer = 0  # Timer for temporal aggregation
    
    while True:
        # Generate packet with appropriate size
        if size_choice == 0:  
            packet_size = random.randint(10, 100)
        elif size_choice == 1:  
            packet_size = random.randint(101, 500)
        else:  
            packet_size = random.randint(501, 1500)

        packet = Packet(packet_size, src_node.name, dest_node.name)
        packet.creation_time = env.now
        tracker.record_generated()
        
        # send packet with different strategies
        
        if strategy == "periodic":
            env.process(src_node.send_packet(packet, next_hop=dest_node, tracker=tracker))
            yield env.timeout(random.expovariate(1))
            
        elif strategy == "threshold":
            if last_sent_data is None or abs(packet.size - last_sent_data) > threshold:
                env.process(src_node.send_packet(packet, next_hop=dest_node, tracker=tracker))
                last_sent_data = packet.size

        elif strategy == "temporal_aggregation":
            accumulated_data.append(packet)
            aggregation_timer += 1

            if aggregation_timer >= aggregation_interval:
                aggregated_size = sum(pkt.size for pkt in accumulated_data)
                aggregated_packet = Packet(aggregated_size, src_node.name, dest_node.name)
                aggregated_packet.creation_time = env.now  
                env.process(src_node.send_packet(aggregated_packet, next_hop=dest_node, tracker=tracker))
                accumulated_data = []
                aggregation_timer = 0
        
        yield env.timeout(random.expovariate(lambda_val))