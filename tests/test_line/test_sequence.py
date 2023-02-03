"""Tests a sequence of line commands."""

from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory print('test'); 1 + 1")


def test_notebook(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -n print('test'); 1 + 1")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n print('test'); 1 + 1")


def test_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -j print('test'); 1 + 1")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -j print('test'); 1 + 1")


def test_notebook_jupyter(ipython):
    with tt.AssertPrints("test\nRAM usage: line:"):
        ipython.run_cell("%memory -n -j print('test'); 1 + 1")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n -j print('test'); 1 + 1")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -n -j print('test'); 1 + 1")


def test_notebook_jupyter_table(ipython):
    with tt.AssertPrints("test\nRAM usage |   current   |     peak     |"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test'); 1 + 1")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test'); 1 + 1")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%memory -n -j -t -i 20 print('test'); 1 + 1")
