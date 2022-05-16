import click

@click.group()
def downleth_cli():
    pass

@click.command(name='exec')
@click.argument('config')
def exec_cmd(config: str):
    pass

downleth_cli.add_command(exec_cmd)

def main():
    downleth_cli(obj={})

if __name__ == '__main__':
    main()
