import redis
import json
import time
from database import SessionLocal, Task

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def process_task(task_id, execution_time):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = "running"
        db.commit()

        time.sleep(execution_time)  # Simulating execution time

        task.status = "completed"
        db.commit()

while True:
    task_data = r.lpop("task_queue")
    if task_data:
        task = json.loads(task_data)
        process_task(task["task_id"], task["execution_time"])
