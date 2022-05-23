import click
import json
import asyncio

from downleth.schedule import run_schedule

@click.group()
def downleth_cli():
    pass

@click.command(name='exec')
@click.argument('config')
def exec_cmd(config: str):
    with open(config, 'r') as f:
        res = json.load(f)
    asyncio.run(run_schedule(res))

# TODO: add command to spin up local server to watch lecture live locally, web client is unreliable
downleth_cli.add_command(exec_cmd)

def main():
    downleth_cli(obj={})

if __name__ == '__main__':
    main()
