"""Tests for a cell that consumes a small amount of memory."""

from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints("test\nRAM usage: cell:"):
        ipython.run_cell("%%memory\nprint('test')")


def test_notebook(ipython):
    with tt.AssertPrints("test\nRAM usage: cell:"):
        ipython.run_cell("%%memory -n\nprint('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n\nprint('test')")


def test_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: cell:"):
        ipython.run_cell("%%memory -j\nprint('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -j\nprint('test')")


def test_notebook_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: cell:"):
        ipython.run_cell("%%memory -n -j\nprint('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n -j\nprint('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -n -j\nprint('test')")


def test_notebook_jupyter_table(ipython):
    with tt.AssertPrints("test\nRAM usage |   current   |     peak     |"):
        ipython.run_cell("%%memory -n -j -t -i 20\nprint('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n -j -t -i 20\nprint('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -n -j -t -i 20\nprint('test')")
