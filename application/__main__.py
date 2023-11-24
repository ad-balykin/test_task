import click

from application.app import run_api, create_runners


@click.group()
def cli() -> None:
    pass


@click.command()
def serve() -> None:
    run_api()


@click.command()
def run_runners() -> None:
    create_runners()


if __name__ == "__main__":
    cli.add_command(serve)
    cli.add_command(run_runners)
    cli()
