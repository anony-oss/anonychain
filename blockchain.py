from __future__ import annotations
from hash import Hash
import time
from interface import Node
from transaction import Transaction
from block import Block, GenesisBlock
from miner import Miner


class Blockchain():
    def __init__(self, nodes: list[Node], difficulty: int, address: str):
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []
        self.nodes: list[Node] = nodes
        self.difficulty: int = int(difficulty)
        self.address: str = address
        self.addresses: dict = {}
        
        for node in nodes:
            if len(node.chain().chain) > len(self.chain):
                self.chain = node.chain().chain
        if len(self.chain) == 0:
            self.new_block(0, 0)

    def add_transaction(self, transaction: Transaction | list[Transaction] = None, from_node: bool = False):
        if isinstance(transaction, Transaction):
            self.current_transactions.append(transaction)
            if not from_node:
                print(f'Transaction added to chain: {str(Transaction)}.')
                for node in self.nodes:
                    node.add_transaction(transaction, True)
        elif isinstance(transaction, list):
            transactions = transaction
            for transaction in transactions:
                self.current_transactions.append(transaction)
                print(f'Transaction added to chain: {str(Transaction)}.')
                if not from_node:
                    for node in self.nodes:
                        node.add_transaction(transaction, True)

    def new_block(self, index=None, timestamp=0):
        if index is None:
            index = len(self.chain)
        if timestamp == 0:
            timestamp = time.time()

        # Setting previous block
        if len(self.chain) > 0:
            previous_block = self.chain[-1]
        else:
            previous_block = None

        # Adding mining fee transaction
        if len(self.chain) > 0:
            self.add_transaction(Transaction('0', '0', self.address, 1, '0', time.time(), previous_block.block_hash), True)
            previous_block.calculate()
        
        # Creating new block
        block = Block(index, timestamp, self.current_transactions,
                      previous_block=previous_block)
        block.hash()
        
        # Resolving chain
        self.resolve()
        print('Resolved successfully.')
        
        # Mining block
        miner = Miner(self.difficulty)
        salt = miner.mine(block.block_hash)
        block.salt = salt
        print('Block mined successfully.')
        
        # Reseting current transaction and adding block to chain
        self.current_transactions = []
        self.chain.append(block)
        
        # Updating addresses list
        self.addresses = block.addresses
        
    def genesis(self):
        self.chain.append(GenesisBlock())
        
    def resolve(self, from_node: bool = False):
        for node in self.nodes:
            blockchain = node.chain()
            chain = blockchain.chain
            
            if len(chain) > len(self.chain):
                valid = True
                for block in chain:
                    hash = Hash((block.block_hash + '|' + str(block.salt)).encode('ascii'))
                    if not hash.hash.endswith('0' * self.difficulty):
                        if not from_node:
                            node.resolve(True)
                        valid = False
                if valid:
                    self.chain = chain
                    self.addresses = blockchain.addresses
        # mx = None
        # for chain in chains:
        #     if mx is None:
        #         mx = chain
            
        #     print(f'Chain with {chains[chain][0]} copies and {chains[chain][1]} blocks.')
        #     if chains[chain][1] > chains[mx][1]:
        #         mx = chain
        #         print('Finded longer chain.')
        #     elif chains[chain][1] == chains[mx][1] and chains[chain][0] > chains[mx][0]:
        #         mx = chain
        #         print('More popular chain.')
        # if mx is not None:
        #     self.chain = list(mx)
        