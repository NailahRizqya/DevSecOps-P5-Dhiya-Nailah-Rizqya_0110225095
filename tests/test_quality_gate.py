import json

from scripts import quality_gate as qg


def _report(*severities):
    return {
        "results": [
            {
                "issue_severity": s,
                "test_id": "B000",
                "filename": "x.py",
                "line_number": 1,
                "issue_text": "contoh",
            }
            for s in severities
        ]
    }


def test_clean_report_passes():
    _, violations = qg.evaluate(_report())
    assert violations == []


def test_high_fails():
    _, violations = qg.evaluate(_report("HIGH"))
    assert len(violations) == 1


def test_medium_fails_and_low_tolerated():
    assert qg.evaluate(_report("LOW", "LOW"))[1] == []
    assert len(qg.evaluate(_report("MEDIUM"))[1]) == 1
    assert len(qg.evaluate(_report(*["LOW"] * 6))[1]) == 1


def test_main_exit_codes(tmp_path, capsys):
    ok = tmp_path / "ok.json"
    bad = tmp_path / "bad.json"
    ok.write_text(json.dumps(_report()))
    bad.write_text(json.dumps(_report("HIGH")))
    assert qg.main([str(ok)]) == 0
    assert qg.main([str(bad)]) == 1
    assert "FAILED" in capsys.readouterr().out
