"""Utility functions."""

from __future__ import annotations

import os

import psutil


def format_bytes(n: int) -> str:
    """Format an integer number of bytes into a string"""

    for unit in ["B", "KiB", "MiB", "GiB"]:
        if not n // 1024:
            return f"{round(n, 2)} {unit}"
        n /= 1024


def get_last_line(file_path: str, skip_empty: bool = False) -> str:
    """Get the last line of a file"""

    with open(file_path, "rb") as file:
        try:
            file.seek(-1, os.SEEK_END)
            while True:
                if file.read(1) == b"\n":
                    if file.read(1) or not skip_empty:
                        file.seek(-1, os.SEEK_CUR)
                        break
                    file.seek(-1, os.SEEK_CUR)
                file.seek(-2, os.SEEK_CUR)
        # one-line case
        except OSError:
            file.seek(0)

        last_line = file.read().strip(b"\n").decode()
        return last_line


def get_jupyter_pids() -> list[int]:
    """Get Jupyter processes ids"""

    jupyter_pids = []

    pids = psutil.pids()
    for pid in pids:
        try:
            process = psutil.Process(pid)
            cmdline = " ".join(process.cmdline()).lower()
            if "jupyter" in cmdline:
                jupyter_pids.append(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return jupyter_pids


def get_jupyter_memory_usage() -> list[int]:
    """Get the total current memory used by Jupyter"""

    jupyter_memory_usages = []

    jupyter_pids = get_jupyter_pids()
    for pid in jupyter_pids:
        process = psutil.Process(pid)
        jupyter_memory_usages.append(process.memory_info().rss)

    jupyter_memory_usage = sum(jupyter_memory_usages)
    return jupyter_memory_usage


def print_memory_usage_info(
    memory_current: int,
    memory_peak: int,
    memory_notebook: int | None,
    memory_notebook_peak: int | None,
    memory_jupyter: int | None,
    memory_jupyter_peak: int | None,
    expr_type: str | None = None,
    print_table: bool = False,
) -> None:

    dash = "     --    "

    memory_current = format_bytes(memory_current) if memory_current is not None else None
    memory_peak = format_bytes(memory_peak) if memory_peak is not None else dash
    memory_notebook = format_bytes(memory_notebook) if memory_notebook is not None else None
    memory_notebook_peak = format_bytes(memory_notebook_peak) if memory_notebook_peak is not None else dash
    memory_jupyter = format_bytes(memory_jupyter) if memory_jupyter is not None else None
    memory_jupyter_peak = format_bytes(memory_jupyter_peak) if memory_jupyter_peak is not None else dash

    if print_table:

        if any([memory_current is not None, memory_notebook is not None, memory_jupyter is not None]):
            print("RAM usage |   current   |     peak     |")
            print("----------------------------------------")
        if memory_current is not None:
            print(f" {expr_type}     | {memory_current:11} | {memory_peak:11}  |")
        if memory_notebook is not None:
            print(f" notebook | {memory_notebook:11} | {memory_notebook_peak:11}  |")
        if memory_jupyter is not None:
            print(f" jupyter  | {memory_jupyter:11} | {memory_jupyter_peak:11}  |")

    else:

        if expr_type is not None:

            if memory_notebook:
                print(f"RAM usage: {expr_type}:     {memory_current:11} / {memory_peak:11}")
                print(f"           notebook: {memory_notebook:11} / {memory_notebook_peak:11}")
                if memory_jupyter:
                    print(f"           jupyter:  {memory_jupyter:11} / {memory_jupyter_peak:11}")
            elif memory_jupyter:
                print(f"RAM usage: {expr_type}:    {memory_current:11} / {memory_peak:11}")
                print(f"           jupyter: {memory_jupyter:11} / {memory_jupyter_peak:11}")
            else:
                print(f"RAM usage: {expr_type}: {memory_current} / {memory_peak}")

        else:

            if memory_notebook:
                print(f"RAM usage: notebook: {memory_notebook}")
                if memory_jupyter:
                    print(f"           jupyter:  {memory_jupyter}")
            elif memory_jupyter:
                print(f"RAM usage: jupyter: {memory_jupyter}")
