"""Print utility functions."""
from typing import Optional


def format_bytes(n_bytes: int) -> str:
    """Format an integer number of bytes into a string."""

    for unit in ["B", "KiB", "MiB", "GiB"]:
        if not n_bytes // 1024:
            return f"{round(n_bytes, 2)} {unit}"  # noqa: WPS237
        n_bytes /= 1024


def print_memory_usage_info(
    memory_current: int,
    memory_peak: int,
    memory_notebook: Optional[int],
    memory_notebook_peak: Optional[int],
    memory_jupyter: Optional[int],
    memory_jupyter_peak: Optional[int],
    expr_type: Optional[str] = None,
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
