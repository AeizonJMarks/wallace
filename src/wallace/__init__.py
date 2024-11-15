#### META: Title: Package Initialization
#### META: Version: 0.1.0-alpha
#### META: PATH: src/wallace/__init__.py

"""Wallace - A Human-AI Development Protocol"""

print("Loading wallace package...")  # Debug print
__version__ = '0.1.0-alpha'
print(f"Version set to {__version__}")  # Debug print

# Import core components
from . import core
from . import parser
