
from .db_tool_base import SafeSQLExecutor, UnsafeQueryError

class HeartDiseaseDBTool:
    name = "HeartDiseaseDBTool"
    description = "Run safe SELECT queries on the heart_disease table to answer data/statistics questions."

    def __init__(self, db_path: str, table: str = 'heart_disease'):
        allowed_columns = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','target']
        self.executor = SafeSQLExecutor(db_path=db_path, table=table, allowed_columns=allowed_columns, max_rows=500)

    def run(self, user_question: str) -> str:
        q = user_question.lower()
        try:
            if 'average' in q or 'mean' in q:
                if 'age' in q:
                    res = self.executor.execute(f"SELECT AVG(age) as avg_age FROM {self.executor.table} LIMIT 1")
                    if res['rows'] and res['rows'][0].get('avg_age') is not None:
                        return f"Average age: {float(res['rows'][0].get('avg_age')):.2f}"
                return "I could not parse an average request. Try: 'Average age of patients' or 'Average cholesterol where target=1'."
            if 'count' in q or 'how many' in q:
                res = self.executor.execute(f"SELECT COUNT(*) as count FROM {self.executor.table}")
                return f"Count: {res['rows'][0].get('count')}"
            if 'sample' in q or 'show' in q or 'example' in q:
                res = self.executor.safe_select(limit=10)
                rows = res['rows'][:10]
                if not rows:
                    return "No rows found."
                return "\n".join([str(r) for r in rows])
            res = self.executor.safe_select(limit=5)
            return "Preview:\n" + "\n".join([str(r) for r in res['rows']])
        except UnsafeQueryError as e:
            return f"Unsafe query blocked: {e}"
        except Exception as e:
            return f"Error running query: {e}"
