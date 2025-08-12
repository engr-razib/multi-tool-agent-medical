
from .db_tool_base import SafeSQLExecutor, UnsafeQueryError

class CancerDBTool:
    name = "CancerDBTool"
    description = "Run safe SELECT queries on the cancer table to answer data/statistics questions."

    def __init__(self, db_path: str, table: str = 'cancer'):
        allowed_columns = ['id','radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','diagnosis']
        self.executor = SafeSQLExecutor(db_path=db_path, table=table, allowed_columns=allowed_columns, max_rows=500)

    def run(self, user_question: str) -> str:
        q = user_question.lower()
        try:
            if 'average' in q or 'mean' in q:
                for col in ['radius_mean','texture_mean','area_mean','perimeter_mean']:
                    if col in q:
                        res = self.executor.execute(f"SELECT AVG({col}) as avg_{col} FROM {self.executor.table} LIMIT 1")
                        return f"Average {col}: {res['rows'][0].get('avg_'+col)}"
                return "Specify which metric to average, e.g. 'average radius_mean'"
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
