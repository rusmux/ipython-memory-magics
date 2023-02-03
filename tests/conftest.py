import subprocess

import pytest
from IPython import get_ipython
from IPython.terminal.interactiveshell import TerminalInteractiveShell


@pytest.fixture(scope="session")
def ipython():
    subprocess.Popen(["jupyter", "notebook", "--no-browser"])
    TerminalInteractiveShell.instance()
    ipython_ = get_ipython()
    ipython_.run_cell("%load_ext memory_magics")
    return ipython_
