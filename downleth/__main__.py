import click
import json

from downleth.download import Downloader

@click.group()
def downleth_cli():
    pass

@click.command(name='exec')
@click.argument('config')
def exec_cmd(config: str):
    with open(config, 'r') as f:
        res = json.load(f)
    d = Downloader(res)

downleth_cli.add_command(exec_cmd)

def main():
    downleth_cli(obj={})

if __name__ == '__main__':
    main()
