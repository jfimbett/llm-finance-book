import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"


def cik_pad(cik):
    digits = "".join(ch for ch in str(cik) if ch.isdigit())
    if not digits:
        die(f"invalid CIK: {cik!r}")
    return digits.rjust(10, "0")


def data_dir(cik):
    d = DATA_ROOT / cik_pad(cik)
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))
    return path


def read_json(path):
    return json.loads(Path(path).read_text())


def emit(obj):
    print(json.dumps(obj, indent=2))


def die(msg):
    print(json.dumps({"error": str(msg)}))
    sys.exit(1)


def sec_headers():
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua or ua.startswith("REPLACE"):
        die("SEC_USER_AGENT env var not set. Set it to e.g. 'Your Name you@example.com'")
    return {"User-Agent": ua, "Accept-Encoding": "gzip, deflate"}
