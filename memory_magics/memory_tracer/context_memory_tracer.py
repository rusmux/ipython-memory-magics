"""Implementation of a memory tracer as a context manager."""

from __future__ import annotations

import os
import subprocess

from tempfile import mkstemp
from time import sleep
from typing import Iterable

from ..utils import get_last_line
from . import _memory_tracer


class ContextMemoryTracer:
    """Context Manager to trace Jupyter notebook peak memory usage."""

    def __init__(self, pids: Iterable[int], interval: float = 10.0) -> None:
        self.pids: Iterable[int] = pids
        self.interval: float = interval

        self.memory_usages_peak: dict[int, int] = {}
        self.total_peak: int | None = None

        self._file_handle: int | None = None
        self._file_path: str | None = None
        self._process: subprocess.Popen | None = None

    def __enter__(self) -> None:
        self._file_handle, self._file_path = mkstemp()

        cmdline = [
            "python",
            _memory_tracer.__file__,
            *map(str, self.pids),
            self._file_path,
            "--interval",
            str(self.interval),
        ]

        self._process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sleep(0.1)  # for script to load

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._process.terminate()

        stream = self._process.communicate()
        return_code = self._process.returncode

        if return_code != -15:
            raise NotImplementedError(stream[-1])

        memory_usages_peak = get_last_line(self._file_path, skip_empty=True).split()
        memory_usages_peak = list(map(int, memory_usages_peak))
        memory_usages_peak, total_peak = memory_usages_peak[:-1], memory_usages_peak[-1]

        os.close(self._file_handle)
        os.remove(self._file_path)

        self.memory_usages_peak = dict(zip(self.pids, memory_usages_peak))
        self.total_peak = total_peak
