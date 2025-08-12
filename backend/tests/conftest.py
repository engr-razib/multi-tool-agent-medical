
import pytest
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / 'backend'
DB_DIR = ROOT / 'dbs'
DB_DIR.mkdir(parents=True, exist_ok=True)

def create_sample_db(db_path, table, columns, rows):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cols_def = ','.join([f"{c} TEXT" for c in columns])
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols_def})")
    for r in rows:
        placeholders = ','.join(['?'] * len(r))
        cur.execute(f"INSERT INTO {table} VALUES ({placeholders})", tuple(map(str, r)))
    conn.commit()
    conn.close()

@pytest.fixture(scope='session', autouse=True)
def setup_test_dbs(tmp_path_factory):
    base = tmp_path_factory.mktemp('data')
    dbdir = base / 'dbs'
    dbdir.mkdir()
    heart_db = dbdir / 'heart_disease.db'
    create_sample_db(str(heart_db), 'heart_disease', ['age','sex','chol','target'], [[63,'1','233','1'],[67,'1','286','1']])
    cancer_db = dbdir / 'cancer.db'
    create_sample_db(str(cancer_db), 'cancer', ['id','radius_mean','diagnosis'], [[1,'12.3','M'],[2,'13.5','B']])
    diabetes_db = dbdir / 'diabetes.db'
    create_sample_db(str(diabetes_db), 'diabetes', ['pregnancies','glucose','age','outcome'], [[6,'148','50','1'],[1,'85','31','0']])
    return {'db_dir': str(dbdir)}
