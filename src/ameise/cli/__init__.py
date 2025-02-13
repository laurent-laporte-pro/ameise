# SPDX-FileCopyrightText: 2024-present Laurent LAPORTE <laurent.laporte.pro@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from ameise.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Ameise")
def ameise():
    click.echo("Hello world!")
