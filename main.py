import sys
import os

# Ensure project root is in PYTHONPATH (Windows fix)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from mcp_server.api_server import app

# 🔑 This variable MUST be named "app"
