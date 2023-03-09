import json

from flask import Flask, request

app = Flask(__name__)

MEMORY = {}


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
  return "[]", 200


@app.route("/tasks/", methods=["POST"])
def add_task():
  payload = request.get_json(force=True)
  task_id = 1
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
