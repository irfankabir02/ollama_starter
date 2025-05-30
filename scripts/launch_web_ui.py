#!/usr/bin/env python3
# scripts/launch_web_ui.py

import sys, os

# Ensure the project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from web.ui import launch_ui

if __name__ == '__main__':
    launch_ui()

