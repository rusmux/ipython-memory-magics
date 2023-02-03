import os
from contextlib import suppress
from typing import List

import psutil


def get_jupyter_memory_usage() -> List[int]:
    """Get the total current memory used by Jupyter"""

    jupyter_memory_usages = []

    jupyter_pids = get_jupyter_pids()
    for pid in jupyter_pids:
        process = psutil.Process(pid)
        jupyter_memory_usages.append(process.memory_info().rss)

    return sum(jupyter_memory_usages)


def get_jupyter_pids() -> List[int]:
    """Get Jupyter processes ids"""

    jupyter_pids = []

    pids = psutil.pids()
    for pid in pids:
        with suppress(psutil.NoSuchProcess, psutil.AccessDenied):
            process = psutil.Process(pid)
            cmdline = " ".join(process.cmdline()).lower()
            if "jupyter" in cmdline:
                jupyter_pids.append(pid)

    return jupyter_pids


def get_last_line(file_path: str, skip_empty: bool = False) -> str:
    """Get the last line of a file."""

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

        return file.read().strip(b"\n").decode()
