from __future__ import annotations

import sys
from pathlib import Path

# Put code/practicals/ on sys.path so `import _verify...` works under pytest.
PRACTICALS_DIR = Path(__file__).resolve().parents[2]
if str(PRACTICALS_DIR) not in sys.path:
    sys.path.insert(0, str(PRACTICALS_DIR))
