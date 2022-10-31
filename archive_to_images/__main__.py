from typing import List

from enum import Enum

import typer
from rich.console import Console

from archive_to_images import version
from archive_to_images.restorer import Restorer
from archive_to_images.transformer import Transformer


class ChunkSize(str, Enum):
    size_0 = "0.5"
    size_1 = "1"
    size_2 = "2"
    size_3 = "5"
    size_4 = "10"


app = typer.Typer(
    name="archive-to-images",
    help="archive-to-images` is a Python cli/package to transform archives into images and reverse.",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]archive-to-images[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="transform")
def transform(
    files: List[str] = typer.Option(
        ...,
        "-f",
        "--files",
        case_sensitive=False,
        help="Files to be archived.",
    ),
    name: str = typer.Option(
        ...,
        "-n",
        "--name",
        case_sensitive=False,
        help="Name of the archive.",
    ),
    size: ChunkSize = typer.Option(
        "1",
        "-s",
        "--size",
        case_sensitive=False,
        help="Maximum size of an image in MB.",
    ),
    password: bool = typer.Option(
        None,
        "-p",
        "--password",
        is_eager=True,
        help="Protect archive with password.",
    ),
    verbose: bool = typer.Option(
        None,
        "-v",
        "--verbose",
        is_eager=True,
        help="Enable verbose output.",
    ),
) -> None:
    """Transforms an archive into multiple images."""
    if password:
        password = typer.prompt(
            "Enter archive password", confirmation_prompt=True, hide_input=True
        )
    Transformer(files, name, int(float(size) * 1024), password, verbose).process()


@app.command(name="restore")
def restore(
    images: List[str] = typer.Option(
        None,
        "-i",
        "--images",
        case_sensitive=False,
        help="Images to restore an archive.",
    ),
    verbose: bool = typer.Option(
        None,
        "-v",
        "--verbose",
        is_eager=True,
        help="Enable verbose output.",
    ),
) -> None:
    """Restores an archive from multiple images."""
    Restorer(images, verbose).process()


@app.callback()
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the archive-to-images package.",
    ),
) -> None:
    return


if __name__ == "__main__":
    app()
