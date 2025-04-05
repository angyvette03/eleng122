class Packet:
    def __init__(self, size, src, dest):
        self.size = size
        self.src = src
        self.dest = dest
        self.creation_time = None
        self.end_time = None
        self.hops = []  # Track the path
    
    def add_hop(self, from_node, to_node):
        self.hops.append((from_node, to_node))
    
        
    
