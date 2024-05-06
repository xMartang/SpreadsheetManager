
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Get the path to the src directory
root_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))

# Add the src directory to sys.path, so we can import the backend modules
sys.path.append(root_path)
