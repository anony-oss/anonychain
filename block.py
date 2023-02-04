from transaction import Transaction
from hash import Hash


class Block():
    def __init__(self, index: int = 0, time: float = 0,
                 transactions: list[Transaction] = None,
                 previous_block = None, salt: int = 0, fee: float = 0):
        if transactions is None:
            transactions = []

        self.index: int = index
        self.time: float = time
        self.transactions: list[Transaction] = transactions
        self.salt: int = salt
        self.calculated: bool = False
        self.fee: float = fee
        self.genesis: bool = False

        self.previous_block: Block = previous_block
        if self.previous_block is not None:
            self.previous_block_hash: str = self.previous_block.get_hash()
            self.addresses = self.previous_block.addresses
        else:
            self.previous_block_hash = '0'
            self.addresses = {}

        self.hash()
        
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def calculate(self):
        if not self.calculated:
            for transaction in self.transactions:
                if transaction.sender not in self.addresses:
                    self.addresses[transaction.sender] = 0
                if transaction.recipient not in self.addresses:
                    self.addresses[transaction.recipient] = 0
                self.addresses[transaction.sender] -= transaction.amount
                self.addresses[transaction.recipient] += transaction.amount
            self.calculated = True
        else:
            print('Block already calculated.')

    def is_valid(self):
        if self.previous_block is not None:
            if self.previous_block.get_hash() != self.previous_block_hash:
                print('Previous block hash is invalid.')
                return False
            if self.previous_block.is_valid() is False:
                print('Previous block is invalid.')
                return False
        if self.get_hash() != self.block_hash:
            print('Self hash is wrong.')
            return False


        for address in self.addresses:
            if self.addresses[address] < 0:
                return False
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False

        return True
    
    def get_hash(self):
        data = str(self.index) + str(self.time) + str(self.transactions) \
            + str(self.previous_block_hash)
        hash = Hash(data.encode('ascii'))
        return hash.hash
        
    def hash(self):
        self.block_hash: str = self.get_hash()
        

class GenesisBlock(Block):
    def __init__(self):
        self.index: int = 0
        self.time: float = 0
        self.transactions: list[Transaction] = []
        self.salt: int = None
        self.calculated: bool = True
        self.fee: float = 0
        self.genesis: bool = False

        self.previous_block: Block = None
        self.previous_block_hash = '0'
        
        self.addresses = {'0': 0}

        self.hash()
    
    def add_transaction(self, transaction):
        pass
    
    def is_valid(self):
        return True
    
    def get_hash(self):
        return '0'