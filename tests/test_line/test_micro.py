"""Tests for a line that consumes a small amount of memory."""

from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory print('test')")


def test_notebook(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -n print('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n print('test')")


def test_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -j print('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -j print('test')")


def test_notebook_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -n -j print('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n -j print('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -n -j print('test')")


def test_notebook_jupyter_table(ipython):
    with tt.AssertPrints("test\nRAM usage |   current   |     peak     |"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test')")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test')")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test')")
