from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
        frozen=True,
    )

    app_name: str = Field(default="SpaceCommsDigitalTwin", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    allowed_origins: List[str] = Field(default=["*"], alias="ALLOWED_ORIGINS")

    auth_secret_key: str = Field(default="change-me", alias="AUTH_SECRET_KEY")
    auth_algorithm: str = Field(default="HS256", alias="AUTH_ALGORITHM")
    auth_token_expire_minutes: int = Field(default=60, alias="AUTH_TOKEN_EXPIRE_MINUTES")

    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_per_minute: int = Field(default=100, alias="RATE_LIMIT_PER_MINUTE")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")
    log_file: Optional[str] = Field(default=None, alias="LOG_FILE")

    quantum_backends: List[str] = Field(
        default=["qiskit", "cirq", "pennylane", "qutip"],
        alias="QUANTUM_BACKENDS",
    )
    default_simulator_shots: int = Field(default=1024, alias="DEFAULT_SIMULATOR_SHOTS")
    max_qubits: int = Field(default=20, alias="MAX_QUBITS")

    owasp_zap_url: str = Field(default="http://localhost:8080", alias="OWASP_ZAP_URL")
    owasp_zap_api_key: str = Field(default="change-me", alias="OWASP_ZAP_API_KEY")

    database_url: str = Field(default="sqlite:///data/simulations.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    prometheus_enabled: bool = Field(default=False, alias="PROMETHEUS_ENABLED")
    sentry_dsn: Optional[str] = Field(default=None, alias="SENTRY_DSN")

    go_grpc_host: str = Field(default="localhost", alias="GO_GRPC_HOST")
    go_grpc_port: int = Field(default=50051, alias="GO_GRPC_PORT")

    @property
    def cors_origins_list(self) -> List[str]:
        if self.allowed_origins == ["*"]:
            return ["*"]
        return self.allowed_origins

    @property
    def log_file_path(self) -> Optional[Path]:
        if self.log_file:
            return Path(self.log_file)
        return None

    @property
    def api_url(self) -> str:
        return f"http://{self.api_host}:{self.api_port}"


