#!/usr/bin/env python3
"""Portable source launcher. Requires Python 3.11+ and uses only stdlib."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from ngegenbrain.cli import main
raise SystemExit(main())
