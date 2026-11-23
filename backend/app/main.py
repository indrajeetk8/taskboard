import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])

class Task(BaseModel):
    title: str

@app.on_event('startup')
def init_db():
    with conn() as c, c.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL)')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/api/tasks')
def list_tasks():
    with conn() as c, c.cursor() as cur:
        cur.execute('SELECT id, title FROM tasks ORDER BY id')
        return [{'id': r[0], 'title': r[1]} for r in cur.fetchall()]

@app.post('/api/tasks')
def add_task(t: Task):
    with conn() as c, c.cursor() as cur:
        cur.execute('INSERT INTO tasks (title) VALUES (%s)', (t.title,))
    return {'ok': True}
