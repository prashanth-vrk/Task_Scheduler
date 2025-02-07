import redis
import json
from database import SessionLocal, Task

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def add_task(execution_time: int):
    db = SessionLocal()
    new_task = Task(execution_time=execution_time, status="queued")
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    r.rpush("task_queue", json.dumps({"task_id": new_task.id, "execution_time": execution_time}))
    return new_task.id

def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    return [{"id": task.id, "execution_time": task.execution_time, "status": task.status} for task in tasks]
