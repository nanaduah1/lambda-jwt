import os
from pathlib import Path

import boto3
from peewee import PostgresqlDatabase
from vaultclient.client import VaultClient

sm_client = boto3.client("secretsmanager")
secrets = sm_client.get_secret_value(os.getenv("AWS_SECRET_ID"))

BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")

VAULT_ACCESS_TOKEN = secrets.get("VAULT_ACCESS_TOKEN", "development_vault_token")
VAULT_API_ENDPOINT = os.environ.get("VAULT_API_ENDPOINT", "https://vault.tdtechgh.com")

CONFIG = VaultClient(
    vault_access_token=VAULT_ACCESS_TOKEN,
    vault_api_endpint=VAULT_API_ENDPOINT,
    default_group="BUYIT_API_SETTINGS",
    env=ENVIRONMENT,
)

SECRET_KEY = CONFIG.get("SECRET_KEY", "X56326Gt-gshag0-9Bx21sw-8Tgsa7565")


def initialize_db():

    DATABASE_CONFIG = dict(
        db_name="deliverydb",
        user=CONFIG.get("DATABASE_USER", "deliveryapi"),
        password=CONFIG.get("DATABASE_PASSWORD"),
        host=CONFIG.get("DATABASE_HOST", "internal-postgres.db.tdtechgh.com"),
        port=CONFIG.get("DATABASE_PORT", 5432),
    )
    db_settings = dict(DATABASE_CONFIG)
    dbname = db_settings.pop("db_name")
    return PostgresqlDatabase(dbname, **db_settings)
