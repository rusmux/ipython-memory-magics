from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints(""):
        ipython.run_cell("%memory")


def test_notebook(ipython):
    with tt.AssertPrints("RAM usage: notebook: "):
        ipython.run_cell("%memory -n")


def test_jupyter(ipython):
    with tt.AssertPrints("RAM usage: jupyter: "):
        ipython.run_cell("%memory -j")


def test_notebook_jupyter(ipython):
    with tt.AssertPrints("RAM usage: notebook: "):
        ipython.run_cell("%memory -n -j")
    with tt.AssertPrints("jupyter: "):
        ipython.run_cell("%memory -n -j")


def test_quiet(ipython):
    with tt.AssertPrints(""):
        ipython.run_cell("%memory -q")


def test_table(ipython):
    with tt.AssertPrints(""):
        ipython.run_cell("%memory -t")


def test_notebook_jupyter_table(ipython):
    with tt.AssertPrints("RAM usage |   current   |     peak     |"):
        ipython.run_cell("%memory -n -j -t")


def test_notebook_jupyter_table_interval(ipython):
    with tt.AssertPrints("RAM usage |   current   |     peak     |"):
        ipython.run_cell("%memory -n -j -t -i 10")
