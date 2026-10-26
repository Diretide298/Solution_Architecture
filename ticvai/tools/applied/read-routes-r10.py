#!/usr/bin/env python3
"""Moved to tools/fix-read-routes.py (r10 lane E round 2, CHG-R10GEN-006): a standing tool, re-run whenever its check names it.

This name is kept because change entries CHG-R10GEN-001..005 cite it; it runs the standing tool with the same arguments.

    python tools/fix-read-routes.py [--apply]
"""
import runpy
import sys
from pathlib import Path

sys.argv[0] = str(Path(__file__).resolve().parents[1] / "fix-read-routes.py")
runpy.run_path(sys.argv[0], run_name="__main__")
