class Config():
    def __init__(self, difficulty, address, block_time, resolve_time, file_path, port, node_address):
        self.difficulty = difficulty
        self.address = address
        self.block_time = block_time
        self.resolve_time = resolve_time
        self.file_path = file_path
        self.port = port
        self.node_address = node_address


# difficulty = 6
# address = ''
# block_time = 30
# resolve_time = 5
# file_path = 'chain_1.json'
# port = 4949
# node_address = ''