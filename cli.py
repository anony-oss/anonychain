import click
from config import Config
from main import start

@click.command()
@click.option("--difficulty", default=1, help="Difficulty of mining.")
@click.option("--address", default='0', help="Anony Chain address.")
@click.option("--block_time", default=30, help="Time for one block.")
@click.option("--resolve_time", default=5, help="Time before resolve.")
@click.option("--file_path", default='chain.json', help="Chain file path.")
@click.option("--port", default=4949, help="Port of server.")
@click.option("--node_address", default='http://127.0.0.1:4949', help="IP with port of server.")
def main(difficulty, address, block_time, resolve_time, file_path, port, node_address):
    """Start node."""
    config = Config(difficulty=difficulty, address=address, block_time=block_time, resolve_time=resolve_time, file_path=file_path, port=port, node_address=node_address)
    start(config)


if __name__ == '__main__':
    main()