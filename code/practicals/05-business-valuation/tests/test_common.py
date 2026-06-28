import json
import pytest
import _common


def test_cik_pad_from_int():
    assert _common.cik_pad(320193) == "0000320193"


def test_cik_pad_from_padded_string():
    assert _common.cik_pad("CIK0000320193") == "0000320193"


def test_write_then_read_roundtrip(tmp_path):
    p = tmp_path / "x.json"
    _common.write_json(p, {"a": 1})
    assert _common.read_json(p) == {"a": 1}


def test_die_exits_nonzero_with_error_json(capsys):
    with pytest.raises(SystemExit) as e:
        _common.die("boom")
    assert e.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert out == {"error": "boom"}


def test_sec_headers_requires_env(monkeypatch):
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)
    with pytest.raises(SystemExit):
        _common.sec_headers()


def test_sec_headers_uses_env(monkeypatch):
    monkeypatch.setenv("SEC_USER_AGENT", "Tester t@example.com")
    assert _common.sec_headers()["User-Agent"] == "Tester t@example.com"
