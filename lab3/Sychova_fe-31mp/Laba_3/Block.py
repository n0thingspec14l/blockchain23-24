from LABA3.hash import MerkleTree, hash_data


class Block:
    def __init__(self, transactions, previous_hash=''):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_tree = MerkleTree()
        for transaction in transactions:
            self.merkle_tree.add(transaction.__repr__())
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.previous_hash}{self.nonce}{self.merkle_tree.root_hash()}"
        return hash_data(block_string)

    def proof_of_work(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block with PoW: {self.hash}")
