from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class SqlServerConfig:
    driver: str
    server: str
    database: str
    trusted_connection: bool
    username: str
    password: str
    trust_server_certificate: bool

    def connection_string(self) -> str:
        parts = [
            f"DRIVER={{{self.driver}}}",
            f"SERVER={self.server}",
            f"DATABASE={self.database}",
            f"TrustServerCertificate={'yes' if self.trust_server_certificate else 'no'}",
        ]

        if self.trusted_connection:
            parts.append("Trusted_Connection=yes")
        else:
            parts.extend([f"UID={self.username}", f"PWD={self.password}"])

        return ";".join(parts)


@dataclass(frozen=True)
class HuggingFaceConfig:
    token: str
    sentiment_model: str
    ner_model: str
    sarcasm_model: str
    abuse_model: str


@dataclass(frozen=True)
class AppConfig:
    hugging_face: HuggingFaceConfig
    sql_server: SqlServerConfig


def load_config() -> AppConfig:
    load_dotenv_file(Path(".env"))
    return AppConfig(
        hugging_face=HuggingFaceConfig(
            token=os.getenv("HF_TOKEN", os.getenv("PARALLELDOTS_API_KEY", "")).strip(),
            sentiment_model=os.getenv(
                "HF_SENTIMENT_MODEL",
                "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            ).strip(),
            ner_model=os.getenv("HF_NER_MODEL", "dslim/bert-base-NER").strip(),
            sarcasm_model=os.getenv("HF_SARCASM_MODEL", "helinivan/english-sarcasm-detector").strip(),
            abuse_model=os.getenv("HF_ABUSE_MODEL", "unitary/toxic-bert").strip(),
        ),
        sql_server=SqlServerConfig(
            driver=os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server").strip(),
            server=os.getenv("SQLSERVER_SERVER", "localhost").strip(),
            database=os.getenv("SQLSERVER_DATABASE", "TextAnalysisDb").strip(),
            trusted_connection=_get_bool("SQLSERVER_TRUSTED_CONNECTION", default=True),
            username=os.getenv("SQLSERVER_USERNAME", "").strip(),
            password=os.getenv("SQLSERVER_PASSWORD", "").strip(),
            trust_server_certificate=_get_bool("SQLSERVER_TRUST_SERVER_CERTIFICATE", default=True),
        ),
    )


def load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#") or "=" not in stripped_line:
            continue

        key, value = stripped_line.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "y", "on"}
