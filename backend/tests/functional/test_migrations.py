import uuid

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, make_url, text
from sqlalchemy.engine import Engine

from app.core.config import settings


# Define verification functions for specific migrations
def verify_create_users_table(engine: Engine) -> None:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables, "Users table should exist"

    columns = [c["name"] for c in inspector.get_columns("users")]
    expected_columns = ["id", "name", "email", "hashed_password"]
    for col in expected_columns:
        assert col in columns, f"Column {col} missing in users table"


# Map Revision ID -> Verification Function
MIGRATION_TESTS = {
    "374a3aa5941b": verify_create_users_table,
}


def test_migrations_step_by_step(monkeypatch: pytest.MonkeyPatch) -> None:
    # 1. Prepare Configuration
    # We use the main Postgres instance but create a unique DB for this migration test
    # to avoid conflicting with parallel functional tests.

    unique_id = str(uuid.uuid4()).replace("-", "")
    test_db_name = f"test_migration_{unique_id}"

    # Parse the configured DATABASE_URL
    db_url = make_url(settings.DATABASE_URL)

    # Connect to 'postgres' (admin DB) to create the new test DB
    # We need a SYNC driver for create_engine (admin)
    # The default driver might be asyncpg if configured that way.
    # We force a sync driver (e.g. psycopg2 implicit in 'postgresql://')
    # make_url doesn't easily swap driver like that without manipulation.

    # Logic:
    # 1. Construct admin URL (postgres DB) using sync driver
    # 2. Construct target URL (test DB) using sync driver (for inspection)
    # 3. Construct target URL (test DB) using ASYNC driver (for env.py / alembic)

    # Assuming host/port/user/pass are same.
    # Let's rebuild the string manually or via URL object setter

    # URL object from make_url(settings.DATABASE_URL) -> postgresql+asyncpg://...

    # Admin URL (Sync): postgresql://user:pass@host:port/postgres
    admin_url = db_url.set(
        drivername="postgresql", database="postgres"
    ).render_as_string(hide_password=False)

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        conn.execute(text(f"CREATE DATABASE {test_db_name}"))
    admin_engine.dispose()

    # Target URL (Sync) for inspection in this test
    # postgresql://user:pass@host:port/test_db_name
    target_db_url = db_url.set(
        drivername="postgresql", database=test_db_name
    ).render_as_string(hide_password=False)

    # Target URL (Async) for Alembic env.py
    # postgresql+asyncpg://user:pass@host:port/test_db_name
    # (Assuming original URL had +asyncpg or similar, we keep original driver)
    async_target_db_url = db_url.set(database=test_db_name).render_as_string(
        hide_password=False
    )

    monkeypatch.setenv("DATABASE_URL", async_target_db_url)

    # Sync engine for inspection/verification in THIS test function
    engine = create_engine(target_db_url)

    try:
        # Load Alembic Config
        alembic_cfg = Config("alembic.ini")
        # Ensure it uses the stdout for output so we can see it if needed, or silence it
        # alembic_cfg.set_main_option("script_location", "migrations") # should be in ini

        # Initialize ScriptDirectory
        script = ScriptDirectory.from_config(alembic_cfg)

        # Get revisions
        revisions = list(script.walk_revisions("base", "head"))
        revisions.reverse()

        # --- UPGRADE PHASE ---
        for rev in revisions:
            command.upgrade(alembic_cfg, rev.revision)

            if rev.revision in MIGRATION_TESTS:
                MIGRATION_TESTS[rev.revision](engine)

        # Verify Head
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            current_ver = result.scalar()
            assert current_ver == revisions[-1].revision

        # --- DOWNGRADE PHASE ---
        for rev in reversed(revisions):
            downgrade_target = rev.down_revision if rev.down_revision else "base"
            command.downgrade(alembic_cfg, str(downgrade_target))

            if downgrade_target == "base":
                inspector = inspect(engine)
                assert "users" not in inspector.get_table_names()

    finally:
        # Cleanup
        engine.dispose()
        # Drop DB
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        admin_engine.dispose()
