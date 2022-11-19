from IPython import get_ipython
import pkg_resources
from .compare import compare
from .sw_cellmagic import CompareViewMagic

__version__: str = pkg_resources.get_distribution(__name__).version

print(f"Jupyter compare_view v{__version__}")

try:
    ipy = get_ipython()
    ipy.register_magics(CompareViewMagic)
except AttributeError:
    print("Can not load CompareViewMagic because this is not a notebook")


