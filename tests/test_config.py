import json

import pytest

from whispernote.config import CONFIG_FILENAME, load_models_config


def test_explicit_config_wrong_basename(tmp_path):
    bad = tmp_path / "other.json"
    bad.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_models_config(str(bad))
    assert CONFIG_FILENAME in str(exc.value)
    assert "other.json" in str(exc.value) or "basename" in str(exc.value).lower()


def test_explicit_config_missing_file(tmp_path):
    missing = tmp_path / CONFIG_FILENAME
    with pytest.raises(ValueError) as exc:
        load_models_config(str(missing))
    assert "not found" in str(exc.value).lower()


def test_explicit_config_loads(tmp_path):
    p = tmp_path / CONFIG_FILENAME
    p.write_text(
        json.dumps({"asr_model": "x", "diarization_model": "y"}),
        encoding="utf-8",
    )
    cfg = load_models_config(str(p))
    assert cfg == {"asr_model": "x", "diarization_model": "y"}


def test_auto_discovery_cwd_first(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cwd_file = tmp_path / CONFIG_FILENAME
    cwd_file.write_text('{"asr_model": "from_cwd"}', encoding="utf-8")
    global_dir = tmp_path / ".config" / "whispernote"
    global_dir.mkdir(parents=True)
    global_file = global_dir / CONFIG_FILENAME
    global_file.write_text('{"asr_model": "from_global"}', encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path))
    # ~/.config/whispernote expands from HOME
    cfg = load_models_config(None)
    assert cfg["asr_model"] == "from_cwd"


def test_auto_discovery_global_when_no_cwd_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    global_dir = tmp_path / ".config" / "whispernote"
    global_dir.mkdir(parents=True)
    global_file = global_dir / CONFIG_FILENAME
    global_file.write_text('{"asr_model": "from_global_only"}', encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = load_models_config(None)
    assert cfg["asr_model"] == "from_global_only"


def test_explicit_config_does_not_fallback(tmp_path, monkeypatch):
    """Missing --config path must not load ./whispernote.json."""
    monkeypatch.chdir(tmp_path)
    fallback = tmp_path / CONFIG_FILENAME
    fallback.write_text('{"asr_model": "fallback"}', encoding="utf-8")
    missing = tmp_path / "subdir" / CONFIG_FILENAME
    with pytest.raises(ValueError):
        load_models_config(str(missing))
    # cwd file ignored when explicit path was wrong/missing
    cfg = load_models_config(None)
    assert cfg["asr_model"] == "fallback"
