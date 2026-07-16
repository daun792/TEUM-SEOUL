from app.core.config import Settings


def test_cors_origins_accepts_comma_separated_environment(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://a.example,https://b.example")

    settings = Settings(_env_file=None)

    assert settings.cors_origins == ["https://a.example", "https://b.example"]
