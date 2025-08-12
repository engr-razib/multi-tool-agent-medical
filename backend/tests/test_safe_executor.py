
from backend.app.tools.db_tool_base import SafeSQLExecutor, UnsafeQueryError
import os
import sqlite3
import pytest

def test_safe_select_and_blocking(tmp_path, setup_test_dbs):
    dbdir = setup_test_dbs['db_dir']
    heart_db = os.path.join(dbdir, 'heart_disease.db')
    executor = SafeSQLExecutor(db_path=heart_db, table='heart_disease', allowed_columns=['age','sex','chol','target'], max_rows=10)
    res = executor.safe_select(select_cols=['age','chol'], filters={'target':'1'}, limit=5)
    assert 'columns' in res and 'rows' in res
    with pytest.raises(UnsafeQueryError):
        executor.execute('DROP TABLE heart_disease')
    with pytest.raises(UnsafeQueryError):
        executor.execute('SELECT * FROM heart_disease; DELETE FROM heart_disease')
