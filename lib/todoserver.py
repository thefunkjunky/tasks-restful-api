import json
import random

from flask import Flask, request

app = Flask(__name__)

MEMORY = {}


def gen_task_id():
  task_id = random.getrandbits(64)
  if task_id in MEMORY:
    task_id = gen_task_id()
  return task_id


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
  tasks = [
    {
      "id": task_id,
      "summary": task["summary"]
    }
    for task_id, task in MEMORY.items()
  ]
  return json.dumps(tasks), 200


@app.route("/tasks/", methods=["POST"])
def add_task():
  payload = request.get_json(force=True)
  task_id = gen_task_id()
  MEMORY[task_id] = {
    "summary": payload["summary"],
    "description": payload["description"]
  }
  task_info = {"id": task_id}
  return json.dumps(task_info), 201


@app.route("/tasks/<int:task_id>/", methods=["GET"])
def get_task(task_id):
  task_info = MEMORY[task_id].copy()
  task_info["id"] = task_id
  return json.dumps(task_info), 200


if __name__ == '__main__':
  app.run()
