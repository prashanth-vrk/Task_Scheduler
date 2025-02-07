import redis
import json
from database import SessionLocal, Task

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def schedule_tasks():
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.status == "queued").all()

    tasks = sorted(tasks, key=lambda x: x.execution_time)  # SRTF scheduling

    for task in tasks:
        r.rpush("task_queue", json.dumps({"task_id": task.id, "execution_time": task.execution_time}))
        task.status = "scheduled"
        db.commit()
