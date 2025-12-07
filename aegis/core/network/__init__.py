def __init__(self):
        self.graph = nx.DiGraph() # DiGraph is already Directed (One-way)
        self.acls: List[NetworkACL] = [] # Store firewall rules