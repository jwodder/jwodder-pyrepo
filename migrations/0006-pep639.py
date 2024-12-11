#!/usr/bin/env pipx run
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "click ~= 8.0",
#     "in-place ~= 1.0",
# ]
# ///

from __future__ import annotations
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any
import click
from in_place import InPlace


@click.command()
@click.option("--git/--no-git", default=True)
@click.argument(
    "dirpath",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=os.curdir,
)
def main(dirpath: Path, git: bool) -> None:
    update_pyproject(dirpath)
    if git:
        log("Committing ...")
        runcmd(
            "git", "commit", "-m", "Update for PEP 639", "pyproject.toml", cwd=dirpath
        )


def update_pyproject(dirpath: Path) -> None:
    log("Updating pyproject.toml ...")
    with InPlace(dirpath / "pyproject.toml", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith("license-files ="):
                line = 'license-files = ["LICENSE"]\n'
            elif line.strip() == '"License :: OSI Approved :: MIT License",':
                continue
            print(line, end="", file=fp)


def runcmd(*args: str | Path, **kwargs: Any) -> None:
    argstrs = [str(a) for a in args]
    click.secho("+" + shlex.join(argstrs), err=True, fg="green")
    r = subprocess.run(argstrs, **kwargs)
    if r.returncode != 0:
        sys.exit(r.returncode)


def log(msg: str) -> None:
    click.secho(msg, err=True, bold=True)


if __name__ == "__main__":
    main()
