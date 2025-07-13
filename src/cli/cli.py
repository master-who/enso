import click

@click.group()
def cli():
    """A simple CLI tool."""
    pass

@cli.command()
def hello():
    """Prints hello message."""
    click.echo("Hello from the CLI!")

if __name__ == "__main__":
    cli()