from blockchain import Blockchain, Transaction, Block
from interface import Node
from crypto import PublicKey
from config import Config
from flask import Flask, request
from helpers import from_chain
import time
import json
import threading


app = Flask(__name__)
running = True

@app.post('/add_transaction')
def add_transaction():
    data = request.json
    
    public_key: PublicKey = PublicKey(string=data['public_key'].encode('ascii'))
    sender: str = data['sender']
    recipient: str = data['recipient']
    amount: float = data['amount']
    signature = data['signature']
    previous_block_hash = data['previous_block_hash']
    addresses = data['addresses']
    transaction_time = data['time']
    from_node = bool(data['from_node'])
    
    if amount > 0:
        balance = blockchain.addresses[sender]
        
        if balance - amount >= 0:
            transaction = Transaction(public_key=public_key, sender=sender, recipient=recipient, amount=amount, signature=signature, time=transaction_time, previous_block_hash=previous_block_hash)
            blockchain.add_transaction(transaction, from_node)
            transaction.addresses = addresses
    
    return {}

@app.post('/resolve')
def resolve():
    blockchain.resolve(request.json['from_node'])
    
    return {}

@app.get('/chain')
def get_chain():
    return json.dumps(blockchain.__dict__, default=to_json)

@app.post('/add_node')
def add_node():
    blockchain.nodes.append(Node(request.json['ip']))
    
    return {}

def to_json(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, Blockchain) or isinstance(obj, Transaction) or isinstance(obj, Block) or isinstance(obj, Node):
        return obj.__dict__
    elif isinstance(obj, PublicKey):
        return obj.get_pem().decode('utf-8')

def main(config: Config):
    global blockchain
    
    try:
        with open(config.file_path, 'r') as file:
            chain = json.load(file)
            blockchain = from_chain(chain)
    except Exception:
        blockchain = Blockchain([], config.difficulty, config.address)
    last_block = time.perf_counter()
    last_resolve = time.perf_counter()
    
    while running:
        if time.perf_counter() - last_block > config.block_time:
            last_block = time.perf_counter()
            print('Generating new block...')
            blockchain.new_block()
            # blockchain.resolve()
            with open(config.file_path, 'w') as file:
                json.dump(blockchain, file, default=to_json)
        if time.perf_counter() - last_resolve > config.resolve_time:
            last_resolve = time.perf_counter()
            print('Resolving...')
            blockchain.resolve()
            with open(config.file_path, 'w') as file:
                json.dump(blockchain, file, default=to_json)

def start(config: Config):
    threading.Thread(target=main, args=(config,)).start()
    threading.Thread(target=app.run, args=('0.0.0.0', config.port)).start()
