
from fastapi import FastAPI
from pydantic import BaseModel
from .agent_runner import route_question

app = FastAPI(title='Multi-Tool Medical AI (safe tools)')

class Query(BaseModel):
    text: str

@app.post('/ask')
async def ask(q: Query):
    answer = route_question(q.text)
    return {'answer': answer}
