from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
import os
try:
    from decouple import config
except ImportError:
    def config(key, default):
        return os.getenv(key, default)

from alembic import context

# Setup correct import path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database.database import Base
# We will import the models here so Alembic can discover them
from app.models.candidate_model import Candidate  # noqa
from app.models.job_model import Job  # noqa
from app.models.screening_model import ScreeningResult  # noqa
# Phase 3 model
try:
    from app.models.user_model import User  # noqa
except ImportError:
    pass

config_alembic = context.config

if config_alembic.config_file_name is not None:
    fileConfig(config_alembic.config_file_name)

target_metadata = Base.metadata

def get_url():
    return config("DATABASE_URL", default="sqlite:///./sql_app.db")

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config_alembic.get_section(config_alembic.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
