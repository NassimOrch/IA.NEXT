"""Portable source-tree launcher for NGeGenBrain_v2."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
from nggegenbrain_v2.cli import main
if __name__ == "__main__":
    raise SystemExit(main())
