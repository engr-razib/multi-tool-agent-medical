
"""Safe SQL executor and DBToolBase for SQLite databases."""
from typing import List, Dict, Any, Optional, Tuple
import sqlite3
import re

FORBIDDEN_TOKENS = [";", "insert", "update", "delete", "alter", "drop", "attach", "detach", "pragma", "create", "replace", "merge"]
_SELECT_ONLY_RE = re.compile(r"^\s*select\s+", re.IGNORECASE)

class UnsafeQueryError(Exception):
    pass

class SafeSQLExecutor:
    def __init__(self, db_path: str, table: str, allowed_columns: List[str], max_rows: int = 100):
        self.db_path = db_path
        self.table = table
        self.allowed_columns = [c.lower() for c in allowed_columns]
        self.max_rows = max_rows

    def _check_sql(self, sql: str):
        low = sql.lower()
        for token in FORBIDDEN_TOKENS:
            if token in low:
                raise UnsafeQueryError(f"Forbidden token in query: {token}")
        if not _SELECT_ONLY_RE.match(sql):
            raise UnsafeQueryError("Only SELECT queries are allowed.")
        if ";" in sql:
            raise UnsafeQueryError("Multiple statements are not allowed.")
        if self.table.lower() not in low:
            raise UnsafeQueryError("Query must reference the allowed table.")

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Dict[str, Any]:
        self._check_sql(sql)
        if re.search(r"\blimit\b", sql, re.IGNORECASE) is None:
            sql = f"{sql.rstrip()} LIMIT {self.max_rows}"
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, params or ())
        rows = [dict(r) for r in cur.fetchall()]
        cols = [d[0] for d in cur.description] if cur.description else []
        conn.close()
        return {"columns": cols, "rows": rows}

    def safe_select(self, select_cols: List[str] = None, filters: Dict[str, Any] = None, order_by: str = None, limit: int = None) -> Dict[str, Any]:
        if select_cols:
            for c in select_cols:
                if c.lower() not in self.allowed_columns:
                    raise UnsafeQueryError(f"Column not allowed: {c}")
            cols_sql = ", ".join(select_cols)
        else:
            cols_sql = "*"

        where_clauses = []
        params = []
        if filters:
            for col, val in filters.items():
                if col.lower() not in self.allowed_columns:
                    raise UnsafeQueryError(f"Filter column not allowed: {col}")
                if isinstance(val, (list, tuple)):
                    placeholders = ",".join(["?"] * len(val))
                    where_clauses.append(f"{col} IN ({placeholders})")
                    params.extend(val)
                else:
                    where_clauses.append(f"{col} = ?")
                    params.append(val)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        order_sql = f"ORDER BY {order_by}" if order_by else ""
        final_limit = min(limit, self.max_rows) if limit and limit > 0 else self.max_rows
        sql = f"SELECT {cols_sql} FROM {self.table} {where_sql} {order_sql} LIMIT {final_limit}"
        return self.execute(sql, tuple(params))
