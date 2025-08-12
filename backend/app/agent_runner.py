
import os
from .tools.heart_tool import HeartDiseaseDBTool
from .tools.cancer_tool import CancerDBTool
from .tools.diabetes_tool import DiabetesDBTool
from .tools.medical_web_search import MedicalWebSearchTool

def make_tools(base_db_dir: str = None):
    base_db_dir = base_db_dir or os.path.join(os.path.dirname(__file__), '..', 'dbs')
    heart_db = os.path.join(base_db_dir, 'heart_disease.db')
    cancer_db = os.path.join(base_db_dir, 'cancer.db')
    diabetes_db = os.path.join(base_db_dir, 'diabetes.db')
    return {
        'heart': HeartDiseaseDBTool(db_path=heart_db),
        'cancer': CancerDBTool(db_path=cancer_db),
        'diabetes': DiabetesDBTool(db_path=diabetes_db),
        'web': MedicalWebSearchTool(),
    }

TOOLS = make_tools()

def route_question(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ['definition','symptoms','treatment','cure','diagnosis']):
        return TOOLS['web'].run(text)
    if 'heart' in t or any(k in t for k in ['chol','trestbps','thalach','age']):
        return TOOLS['heart'].run(text)
    if 'cancer' in t or 'tumor' in t:
        return TOOLS['cancer'].run(text)
    if 'diabetes' in t or 'glucose' in t or 'insulin' in t:
        return TOOLS['diabetes'].run(text)
    return TOOLS['web'].run(text)
