"""
Script for tracing peak memory usage of the specified processes.
The program is running until terminated.
"""

import argparse
from time import sleep
from typing import Iterable

import psutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trace the peak memory usage of a process.")

    parser.add_argument(
        "pids",
        type=int,
        nargs="+",
        help="Ids of the processes to trace peak memory usage of",
    )

    parser.add_argument(
        "output",
        type=str,
        help="Output file to save peak memory usage to",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=10.0,
        nargs="?",
        help="Interval in milliseconds for checking memory usage",
    )

    args = parser.parse_args()
    return args


def trace_peak_memory_usage(
    pids: Iterable[int],
    output: str,
    interval: float = 10.0,
) -> None:
    """Trace memory usage of the specified processes and write peak values to a file."""

    processes = [psutil.Process(pid) for pid in pids]
    memory_usages_current = [0] * len(processes)
    memory_usages_peak = [0] * len(processes)
    total_peak = 0

    line_count = 0
    while True:
        for i, process in enumerate(processes):
            memory_usages_current[i] = process.memory_info().rss
        total_current = sum(memory_usages_current)

        memory_usages_peak = list(map(max, memory_usages_current, memory_usages_peak))  # type: ignore
        total_peak = max(total_current, total_peak)

        file = open(output, "a", encoding="utf-8")
        file.write(" ".join(map(str, memory_usages_peak)) + " " + str(total_peak) + "\n")

        # clear the file so it doesn't get infinitely large
        if line_count > 1000:
            lines = file.readlines()[-10:]
            file.truncate()
            file.seek(0)
            file.writelines(lines)
            line_count = 0

        file.close()

        line_count += 1
        sleep(interval / 1000)


def main() -> None:
    args = parse_args()
    trace_peak_memory_usage(**vars(args))


if __name__ == "__main__":
    main()
