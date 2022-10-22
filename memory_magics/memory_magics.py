"""Main module with memory magic functions for IPython notebooks."""

from __future__ import annotations

import ast
import os
import tracemalloc
from typing import Any

import psutil

from IPython.core.error import UsageError
from IPython.core.magic import (Magics, line_cell_magic, magics_class,
                                needs_local_scope, no_var_expand)

from .memory_tracer import ContextMemoryTracer
from .utils import (get_jupyter_memory_usage, get_jupyter_pids,
                    print_memory_usage_info)


@magics_class
class MemoryMagics(Magics):

    def _compile(self, expr: str) -> tuple[str, str, Any, Any]:
        """Compile a Python statement or expression and get the expression value if any."""

        expr = self.shell.transform_cell(expr)
        expr_ast = self.shell.compile.ast_parse(expr)
        expr_ast = self.shell.transform_ast(expr_ast)

        expr_val = None
        if len(expr_ast.body) == 1 and isinstance(expr_ast.body[0], ast.Expr):
            mode = "eval"
            source = "<memory traced eval>"
            expr_ast = ast.Expression(expr_ast.body[0].value)
        else:
            mode = "exec"
            source = "<memory traced exec>"
            # multi-line %%memory case
            if len(expr_ast.body) > 1 and isinstance(expr_ast.body[-1], ast.Expr):
                expr_val = expr_ast.body[-1]
                expr_ast = expr_ast.body[:-1]
                expr_ast = ast.Module(expr_ast, [])
                expr_val = ast.Expression(expr_val.value)

        code = self.shell.compile(expr_ast, source, mode)

        return mode, source, code, expr_val

    def _trace_memory_usage(
        self, expr: str, local_ns: dict = None, trace_notebooks_peaks: bool = False, interval: float = 10.0
    ) -> tuple[Any, tuple[int, int], tuple[int, int], dict[int, int], int | None]:
        """Trace memory usage of a Python statement or expression execution."""

        tracemalloc.start()
        mode, source, code, expr_val = self._compile(expr)
        compilation_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        glob = self.shell.user_ns
        jupyter_pids = get_jupyter_pids()
        notebooks_memory_peaks = {}
        total_peak = None

        run = eval if mode == "eval" else exec
        try:
            if trace_notebooks_peaks:
                memory_tracer = ContextMemoryTracer(jupyter_pids, interval)
                with memory_tracer:
                    tracemalloc.start()
                    out = run(code, glob, local_ns)
                    traced_memory = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                notebooks_memory_peaks = memory_tracer.memory_usages_peak
                total_peak = memory_tracer.total_peak
            else:
                tracemalloc.start()
                out = run(code, glob, local_ns)
                traced_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
            if expr_val is not None:
                code_2 = self.shell.compile(expr_val, source, "eval")
                out = eval(code_2, glob, local_ns)
        except Exception as error:
            # self.shell.showtraceback()
            raise error

        return out, compilation_memory, traced_memory, notebooks_memory_peaks, total_peak

    def _parse_options(self, line: str = "", cell: str | None = None) -> tuple[dict[str, Any], str]:
        """Parse options from Jupyter magic commands."""

        long_options = ["notebook", "jupyter", "interval=", "table", "quiet"]
        options, line = self.parse_options(line, "nji:tq", *long_options, posix=False)
        parsed_options = {}

        if line and cell:
            raise UsageError("cannot use statement directly after '%%memory'!")

        trace_notebooks_peaks = False
        if any(key in options.keys() for key in ["n", "notebook", "j", "jupyter"]) and (line or cell):
            trace_notebooks_peaks = True
        parsed_options["trace_notebooks_peaks"] = trace_notebooks_peaks

        parsed_options["notebook"] = "n" in options or "notebook" in options
        parsed_options["jupyter"] = "j" in options or "jupyter" in options

        interval = options["i"] if "i" in options else options.get("interval", 10.0)
        try:
            interval = float(interval)
        except ValueError:
            raise TypeError("interval must be int or float") from None
        # for performance reasons
        if interval < 10:
            raise ValueError("interval must be greater than or equal to 10 milliseconds")
        parsed_options["interval"] = interval

        parsed_options["print_table"] = "t" in options or "table" in options
        parsed_options["quiet"] = "q" in options or "quiet" in options

        return parsed_options, line

    @needs_local_scope
    @no_var_expand
    @line_cell_magic
    def memory(self, line: str = "", cell: str | None = None, local_ns: dict | None = None):
        """Trace memory usage of a Python statement or expression execution.

        The current and peak memory usages of a line/cell are printed and the
        value of the expression (if any) is returned.

        This function can be used both as a line and cell magic:

        - In line mode you can trace memory usage of a single-line statement (though multiple
          ones can be chained with using semicolons).

        - In cell mode, you can trace memory usage of the cell body (a directly
          following statement raises an error).

        This function provides very basic functionality. Use the memory_profiler
        module for more control over the measurement.

        User variables are not expanded, the magic line is always left unmodified.

        Options:

        -n <notebook>: If present, show notebook memory usage

        -j <jupyter>: If present, show jupyter memory usage

        -i <interval> Interval in milliseconds for updating memory usage information

        -t <table>: If present, print statistics in a table

        -q <quiet>: If present, do not return the output

        Examples
        --------
        ::

          In [1]: %memory -q list(range(10**6))
          RAM usage: line: 34.33 MiB / 34.33 MiB

          In [2]: %memory -n list(range(10**6)); print('Hello, World!')
          Hello, World!
          RAM usage: line:     2.42 KiB    / 34.33 MiB
                     notebook: 283.86 MiB  / 313.02 MiB

          In [3]: %%memory -n
          RAM usage: notebook: 101.41 MiB

          In [4]: %%memory -n -j -t
                  sum(list(range(10**6)))
          RAM usage |   current   |     peak     |
          ----------------------------------------
           cell     | 2.62 KiB    | 34.33 MiB    |
           notebook | 123.08 MiB  | 155.53 MiB   |
           jupyter  | 170.19 MiB  | 202.55 MiB   |

          Out [4]: 499999500000
        """

        options, line = self._parse_options(line, cell)
        current_pid = os.getpid()

        expr_type = None
        memory_current = None
        memory_peak = None
        memory_notebook = None
        memory_notebook_peak = None
        memory_jupyter = None
        memory_jupyter_peak = None
        out = None

        expr = cell if cell else line
        if expr:
            (
                out,
                compilation_memory,
                traced_memory,
                notebooks_memory_peaks,
                memory_jupyter_peak,
            ) = self._trace_memory_usage(
                expr,
                local_ns,
                options["trace_notebooks_peaks"],
                options["interval"]
            )

            expr_type = "cell" if cell else "line"
            memory_current = traced_memory[0] + compilation_memory[0]

            memory_peak = traced_memory[1] + compilation_memory[0]
            if memory_peak < compilation_memory[1]:
                memory_peak = compilation_memory[1]

            if current_pid in notebooks_memory_peaks:
                memory_notebook_peak = notebooks_memory_peaks[current_pid]

        if options["notebook"]:
            memory_notebook = psutil.Process(current_pid).memory_info().rss

        if options["jupyter"]:
            memory_jupyter = get_jupyter_memory_usage()

        print_memory_usage_info(
            memory_current=memory_current,
            memory_peak=memory_peak,
            memory_notebook=memory_notebook,
            memory_notebook_peak=memory_notebook_peak,
            memory_jupyter=memory_jupyter,
            memory_jupyter_peak=memory_jupyter_peak,
            expr_type=expr_type,
            print_table=options["print_table"],
        )

        if expr and not options["quiet"]:
            return out


def load_ipython_extension(ipython) -> None:
    ipython.register_magics(MemoryMagics)
