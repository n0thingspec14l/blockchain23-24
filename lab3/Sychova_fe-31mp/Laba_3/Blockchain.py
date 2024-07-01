from Block import Block
from collections import defaultdict
from Transaction import Transaction
from hash import MerkleTree


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []  
        self.difficulty = difficulty  
        self.pending_transactions = []  
        self.blockchain_merkle_tree = MerkleTree()
        self.create_genesis_block()

    def create_genesis_block(self):
        initial_transactions = [
            Transaction(sender="System", recipient="Alice", amount=1000, data="Initial balance"),
            Transaction(sender="System", recipient="Bob", amount=500, data="Initial balance")
        ]
        genesis_block = Block(transactions=initial_transactions, previous_hash="0")
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, block):
        block.previous_hash = self.get_latest_block().hash
        block.proof_of_work(self.difficulty)
        self.chain.append(block)
        self.blockchain_merkle_tree.add(block.hash)

    def get_latest_block(self):
        return self.chain[-1]

    def calculate_blockchain_root_hash(self):
        temp_tree = MerkleTree()
        for block in self.chain:
            temp_tree.add(block.hash)
        return temp_tree.root_hash()

    def is_chain_valid(self):
        if self.blockchain_merkle_tree.root_hash() != self.calculate_blockchain_root_hash():
            return False

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def update_balances(self, user_balances, sender, recipient, amount):
        if sender != "System":  
            user_balances[sender]['current'] -= amount
            user_balances[sender]['min'] = min(user_balances[sender]['min'], user_balances[sender]['current'])
            user_balances[sender]['max'] = max(user_balances[sender]['max'], user_balances[sender]['current'])
        user_balances[recipient]['current'] += amount
        user_balances[recipient]['min'] = min(user_balances[recipient]['min'], user_balances[recipient]['current'])
        user_balances[recipient]['max'] = max(user_balances[recipient]['max'], user_balances[recipient]['current'])

    def calculate_balances_until(self, block_number):
        user_balances = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'current': 0})
        for i in range(min(block_number + 1, len(self.chain))):
            for tx in self.chain[i].transactions:
                self.update_balances(user_balances, tx.sender, tx.recipient, tx.amount)
        return user_balances

    def add_transaction(self, transaction):
        if self.calculate_balance(transaction.sender) >= transaction.amount:
            self.pending_transactions.append(transaction)
            print(f"Transaction from {transaction.sender} to {transaction.recipient} for {transaction.amount} added.")
        else:
            print(f"Error: Not enough balance for the transaction from {transaction.sender}.")

    def calculate_balance(self, sender):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == sender:
                    balance -= tx.amount
                if tx.recipient == sender:
                    balance += tx.amount
        for tx in self.pending_transactions:
            if tx.sender == sender:
                balance -= tx.amount
            if tx.recipient == sender:
                balance += tx.amount
        return balance
