import statistics

class PacketTracker:
    def __init__(self):
        self.packets = []
        self.transit_times = []
        self.packet_sizes = []
        self.distances = {}  # Map of (src, dest) -> distance
        self.size_distribution = {
            "small": 0,     # Packets < 100 bytes
            "medium": 0,    # Packets 100-500 bytes
            "large": 0      # Packets > 500 bytes
        }
        
    def record_packet(self, packet, transit_time):
        self.packets.append(packet)
        self.transit_times.append(transit_time)
        self.packet_sizes.append(packet.size)
        if packet.size < 100:
            self.size_distribution["small"] += 1
        elif packet.size <= 500:
            self.size_distribution["medium"] += 1
        else:
            self.size_distribution["large"] += 1
    
    def get_packet_distance(self, packet):
        return len(packet.hops)
    
    def get_size_statistics(self):
        if not self.packet_sizes:
            return {
                "min_size": 0,
                "max_size": 0,
                "avg_size": 0,
                "median_size": 0,
                "size_distribution": self.size_distribution
            }
        else:
            return {
            "min_size": min(self.packet_sizes),
            "max_size": max(self.packet_sizes),
            "avg_size": statistics.mean(self.packet_sizes),
            "median_size": statistics.median(self.packet_sizes),
            "size_distribution": self.size_distribution,
            "size_percentiles": {
                "25th": statistics.quantiles(self.packet_sizes, n=4)[0] if len(self.packet_sizes) >= 4 else 0,
                "50th": statistics.median(self.packet_sizes),
                "75th": statistics.quantiles(self.packet_sizes, n=4)[2] if len(self.packet_sizes) >= 4 else 0,
                "90th": statistics.quantiles(self.packet_sizes, n=10)[8] if len(self.packet_sizes) >= 10 else 0
            }
        }
    
    def get_statistics(self):
        return {
            "total_packets": len(self.packets),
            "total_bytes": sum(self.packet_sizes),
            "avg_packet_size": statistics.mean(self.packet_sizes) if self.packet_sizes else 0,
            "avg_transit_time": statistics.mean(self.transit_times) if self.transit_times else 0,
            "packets_per_second": len(self.packets) / (max([p.end_time for p in self.packets]) if self.packets else 1)
        }