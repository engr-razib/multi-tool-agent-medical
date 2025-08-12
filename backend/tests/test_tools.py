
from backend.app.tools.heart_tool import HeartDiseaseDBTool
from backend.app.tools.cancer_tool import CancerDBTool
from backend.app.tools.diabetes_tool import DiabetesDBTool
import os

def test_heart_tool_avg_and_count(tmp_path, setup_test_dbs):
    dbdir = setup_test_dbs['db_dir']
    heart_db = os.path.join(dbdir, 'heart_disease.db')
    t = HeartDiseaseDBTool(db_path=heart_db)
    out = t.run('What is average age?')
    assert isinstance(out, str)

def test_cancer_tool_sample(tmp_path, setup_test_dbs):
    dbdir = setup_test_dbs['db_dir']
    cancer_db = os.path.join(dbdir, 'cancer.db')
    t = CancerDBTool(db_path=cancer_db)
    out = t.run('Show sample')
    assert isinstance(out, str) or isinstance(out, list)

def test_diabetes_tool_glucose_avg(tmp_path, setup_test_dbs):
    dbdir = setup_test_dbs['db_dir']
    diabetes_db = os.path.join(dbdir, 'diabetes.db')
    t = DiabetesDBTool(db_path=diabetes_db)
    out = t.run('Average glucose')
    assert isinstance(out, str)
