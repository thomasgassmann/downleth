import logging
import click
import json
import asyncio

from downleth.schedule import run_all_schedules

log_formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
root_logger = logging.getLogger()
root_logger.propagate = True
level = logging.DEBUG
root_logger.setLevel(level)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

@click.group()
def downleth_cli():
    pass

@click.command(name='exec')
@click.argument('config')
def exec_cmd(config: str):
    with open(config, 'r') as f:
        res = json.load(f)
    asyncio.run(run_all_schedules(res))

# TODO: add command to spin up local server to watch lecture live locally, web client is unreliable
downleth_cli.add_command(exec_cmd)

def main():
    downleth_cli(obj={})

if __name__ == '__main__':
    main()
