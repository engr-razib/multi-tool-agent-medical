
import pandas as pd
import sqlite3
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "dbs"
DB_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

MAP = {
    "heart_disease.csv": "heart_disease.db",
    "cancer_prediction.csv": "cancer.db",
    "diabetes.csv": "diabetes.db",
}

def convert(csv_filename, db_filename, table_name=None):
    csv_path = DATA_DIR / csv_filename
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}. Place the CSV in backend/data/")
    df = pd.read_csv(csv_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
    db_path = DB_DIR / db_filename
    conn = sqlite3.connect(db_path)
    table_name = table_name or csv_path.stem
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Wrote {csv_path} -> {db_path} (table={table_name})")


if __name__ == '__main__':
    for csv, db in MAP.items():
        if (DATA_DIR / csv).exists():
            convert(csv, db)
        else:
            print(f"Skipping {csv} — not found in backend/data/")
