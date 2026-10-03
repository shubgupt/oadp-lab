import psycopg2
import pytest
import os

# We will run this test against our local Kind cluster via port-forwarding
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def test_extensions_installed_together():
    """
    SPEC REQUIREMENT: The database runtime must support simultaneous initialization
    of both pgvector and pg_duckdb within a single instance.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname="app",
        user="postgres",
        password="testpassword"
    )
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_duckdb;")

    cur.execute(
        "SELECT extname FROM pg_extension WHERE extname IN ('vector', 'duckdb');"
    )
    installed = [row[0] for row in cur.fetchall()]
    
    assert "vector" in installed, "pgvector failed to install"
    assert "duckdb" in installed, "pg_duckdb failed to install"

    cur.close()
    conn.close()
