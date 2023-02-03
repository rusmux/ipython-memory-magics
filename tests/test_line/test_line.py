from IPython.testing import tools as tt


def test_empty(ipython):
    with tt.AssertPrints("RAM usage: line:"):
        ipython.run_cell("%memory print('test')")


def test_notebook(ipython):
    line_command = "%memory -n print('test')"

    with tt.AssertPrints("RAM usage: line:"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("notebook"):
        ipython.run_cell(line_command)


def test_jupyter(ipython):
    line_command = "%memory -j list(range(10**5))"

    with tt.AssertPrints("RAM usage: line:"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("jupyter"):
        ipython.run_cell(line_command)


def test_notebook_jupyter(ipython):
    line_command = "%memory -n -j list(range(10**5))"

    with tt.AssertPrints("RAM usage: line:"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("notebook"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("jupyter"):
        ipython.run_cell(line_command)


def test_notebook_jupyter_table(ipython):
    line_command = "%memory -n -j -t -i 20 list(range(10**5))"

    with tt.AssertPrints("RAM usage |   current   |     peak     |"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("notebook"):
        ipython.run_cell(line_command)
    with tt.AssertPrints("jupyter"):
        ipython.run_cell(line_command)
