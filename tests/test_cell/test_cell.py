from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints("RAM usage: cell:"):
        ipython.run_cell("%%memory\nprint('test')")


def test_notebook(ipython):
    with tt.AssertPrints("RAM usage: cell:"):
        ipython.run_cell("%%memory -n\nlist(range(10**5))")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n\nlist(range(10**5))")


def test_jupyter(ipython):
    with tt.AssertPrints("RAM usage: cell:"):
        ipython.run_cell("%%memory -j\nlist(range(10**5))")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -j\nlist(range(10**5))")


def test_notebook_jupyter(ipython):
    with tt.AssertPrints("RAM usage: cell:"):
        ipython.run_cell("%%memory -n -j\nlist(range(10**5))")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n -j\nlist(range(10**5))")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -n -j\nlist(range(10**5))")


def test_notebook_jupyter_table(ipython):
    with tt.AssertPrints("RAM usage |   current   |     peak     |"):
        ipython.run_cell("%%memory -n -j -t -i 20\nlist(range(10**5))")
    with tt.AssertPrints("notebook"):
        ipython.run_cell("%%memory -n -j -t -i 20\nlist(range(10**5))")
    with tt.AssertPrints("jupyter"):
        ipython.run_cell("%%memory -n -j -t -i 20\nlist(range(10**5))")
