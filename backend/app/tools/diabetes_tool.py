
from .db_tool_base import SafeSQLExecutor, UnsafeQueryError

class DiabetesDBTool:
    name = "DiabetesDBTool"
    description = "Run safe SELECT queries on the diabetes table to answer data/statistics questions."

    def __init__(self, db_path: str, table: str = 'diabetes'):
        allowed_columns = ['pregnancies','glucose','bloodpressure','skinthickness','insulin','bmi','dpf','age','outcome']
        self.executor = SafeSQLExecutor(db_path=db_path, table=table, allowed_columns=allowed_columns, max_rows=500)

    def run(self, user_question: str) -> str:
        q = user_question.lower()
        try:
            if 'average' in q or 'mean' in q:
                if 'glucose' in q:
                    res = self.executor.execute(f"SELECT AVG(glucose) as avg_glucose FROM {self.executor.table} LIMIT 1")
                    return f"Average glucose: {float(res['rows'][0].get('avg_glucose')):.2f}"
                return "Mention a metric like 'glucose' or 'bmi' to average."
            if 'count' in q or 'how many' in q:
                res = self.executor.execute(f"SELECT COUNT(*) as count FROM {self.executor.table}")
                return f"Count: {res['rows'][0].get('count')}"
            if 'sample' in q or 'show' in q:
                res = self.executor.safe_select(limit=10)
                return "\n".join([str(r) for r in res['rows']])
            return self.executor.safe_select(limit=5)['rows']
        except UnsafeQueryError as e:
            return f"Unsafe query blocked: {e}"
        except Exception as e:
            return f"Error: {e}"
