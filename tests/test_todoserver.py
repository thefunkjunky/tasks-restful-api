import unittest
import json

from todoserver import app, MEMORY


def json_body(resp):
  return json.loads(resp.data.decode("utf-8"))


class TestTodoServer(unittest.TestCase):
  def setUp(self):
    MEMORY.clear()
    self.client = app.test_client()
    # verify test pre-conditions
    resp = self.client.get("/tasks/")
    data = json_body(resp)
    self.assertEqual([], data)

  def test_get_empty_list_of_tasks(self):
    resp = self.client.get("/tasks/")
    self.assertEqual(200, resp.status_code)
    data = json_body(resp)
    self.assertEqual([], data)

  def test_create_a_task_and_then_get_its_details(self):
    # create new task
    new_task = {
      "summary": "Get milk.",
      "description": "One gallon organic whole milk."
    }
    resp = self.client.post(
      "/tasks/",
      data=json.dumps(new_task))
    self.assertEqual(201, resp.status_code)
    data = json_body(resp)
    self.assertIn("id", data)
    # get task details
    task_id = data["id"]
    resp = self.client.get(f"/tasks/{task_id:d}/")
    self.assertEqual(200, resp.status_code)
    task = json_body(resp)
    self.assertEqual(task_id, task["id"])
    self.assertEqual(new_task["summary"], task["summary"])
    self.assertEqual(new_task["description"], task["description"])

  def test_create_multiple_tasks_and_fetch_task_list(self):
    # create new tasks
    tasks = [
      {
        "summary": "Get milk.",
        "description": "Half gallon of almond milk."
      },
      {
        "summary": "Go to gym.",
        "description": "Leg day."
      },
      {
        "summary": "Wash car.",
        "description": "Be sure to add wax coat."
      }
    ]

    for task in tasks:
      with self.subTest(task=task):
        resp = self.client.post(
          "/tasks/",
          data=json.dumps(task)
          )
        self.assertEqual(201, resp.status_code)
    resp = self.client.get("/tasks/")
    self.assertEqual(200, resp.status_code)
    checked_tasks = json_body(resp)
    self.assertEqual(3, len(checked_tasks))

