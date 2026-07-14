from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_windows_batch_files_are_ascii_crlf_and_split_by_process():
    expected = {
        "run_local.bat",
        "run_backend.bat",
        "run_frontend.bat",
    }

    assert expected <= {path.name for path in PROJECT_ROOT.glob("*.bat")}

    for name in expected:
        payload = (PROJECT_ROOT / name).read_bytes()
        assert payload.isascii(), f"{name} must be ASCII-safe for legacy Windows cmd code pages"
        assert b"\r\n" in payload, f"{name} must use Windows CRLF line endings"
        assert b"\n" not in payload.replace(b"\r\n", b""), f"{name} contains bare LF line endings"

    launcher = (PROJECT_ROOT / "run_local.bat").read_text(encoding="ascii")
    assert 'start "TeumSeoul API" cmd /k call "%ROOT%run_backend.bat"' in launcher
    assert 'start "TeumSeoul Web" cmd /k call "%ROOT%run_frontend.bat"' in launcher
