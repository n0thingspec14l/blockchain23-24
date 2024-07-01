import hashlib

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

class MerkleNode:
    def __init__(self, left=None, right=None, data=None):
        self.left = left  
        self.right = right  
        self.hash = self.calculate_hash(data)

    def calculate_hash(self, data):
        if data is not None:
            return hash_data(data)
        else:
            return hash_data(self.left.hash + self.right.hash if self.left and self.right else '')

class MerkleTree:
    def __init__(self):
        self.leaves = []  
        self.root = None 

    def add(self, data):
        new_node = MerkleNode(data=data)  
        self.leaves.append(new_node) 
        self.recalculate_tree()  

    def recalculate_tree(self):
        nodes = self.leaves[:]  
        while len(nodes) > 1: 
            if len(nodes) % 2 == 1:
                nodes.append(MerkleNode(data=nodes[-1].hash))
            new_level = []
            for i in range(0, len(nodes), 2):
                new_level.append(MerkleNode(left=nodes[i], right=nodes[i + 1]))
            nodes = new_level
        self.root = nodes[0] if nodes else None  

    def root_hash(self):
        return self.root.hash if self.root else ''
