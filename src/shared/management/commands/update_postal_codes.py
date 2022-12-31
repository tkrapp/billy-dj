"""
Command to update postal codes file
"""

from argparse import ArgumentTypeError
from pathlib import Path
from django.core.management.base import BaseCommand

from shared.helpers.postal_codes import generate_trie


def existing_file(value: str) -> Path:
    """
    Argparse type to return a pathlib.Path object of an existing file.
    """
    path = Path(value)

    if not path.exists():
        raise ArgumentTypeError(f"File {value} does not exists")
    if not path.is_file():
        raise ArgumentTypeError(f"{value} is not a file")

    return path


class Command(BaseCommand):
    """
    Update postal codes command class
    """
    help = "Update postal codes file"

    def add_arguments(self, parser):
        parser.add_argument("-i", "--input", type=existing_file, required=True)
        parser.add_argument("-o", "--output", required=True)

    def handle(self, *args, **options):
        with options["input"].open() as inp:
            trie = generate_trie(inp)

        trie.save(options["output"])
