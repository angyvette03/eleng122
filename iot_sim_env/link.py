class Link:
    def __init__(self, env, bandwidth):
        self.env = env
        self.bandwidth = bandwidth  # Bandwidth in bits per second

    def transmit(self, packet):
        transmission_time = packet.size * 8 / self.bandwidth
        yield self.env.timeout(transmission_time)
        print(f"Packet transmitted from {packet.src} to {packet.dest} in {transmission_time:.2f} seconds")
        