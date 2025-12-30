import pathlib

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


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
# Add new migrations here as they are created
MIGRATION_TESTS = {
    "374a3aa5941b": verify_create_users_table,
}


def test_migrations_step_by_step(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Setup isolated SQLite DB
    db_file = tmp_path / "migration_step_test.db"
    db_url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", db_url)

    # Load Alembic Config
    alembic_cfg = Config("alembic.ini")

    # Create engine for inspection
    engine = create_engine(db_url)

    # Initialize ScriptDirectory to access revision history
    script = ScriptDirectory.from_config(alembic_cfg)

    # Get all revisions from base to head (walk_revisions iterates head -> base)
    revisions = list(script.walk_revisions("base", "head"))
    revisions.reverse()

    # --- UPGRADE PHASE ---
    for rev in revisions:
        # Upgrade to the specific revision
        command.upgrade(alembic_cfg, rev.revision)

        # Run verification checks if defined for this revision
        if rev.revision in MIGRATION_TESTS:
            MIGRATION_TESTS[rev.revision](engine)

    # Verify we are at head
    # (Optional: check alembic_version table)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        current_ver = result.scalar()
        assert current_ver == revisions[-1].revision

    # --- DOWNGRADE PHASE ---
    # Walk backwards from head to base
    for rev in reversed(revisions):
        downgrade_target = rev.down_revision if rev.down_revision else "base"
        command.downgrade(alembic_cfg, str(downgrade_target))

        # After downgrade, we can verify the state is clean relative to that revision
        # For simple check, if we go to base, users should be gone.
        if downgrade_target == "base":
            inspector = inspect(engine)
            assert "users" not in inspector.get_table_names()
