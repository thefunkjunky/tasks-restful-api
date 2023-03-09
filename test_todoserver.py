import unittest
import json

from todoserver import app


def json_body(resp):
  return json.loads(resp.data.decode("utf-8"))


class TestTodoServer(unittest.TestCase):
  def test_get_empty_list_of_tasks(self):
    client = app.test_client()
    resp = client.get("/tasks/")
    self.assertEqual(200, resp.status_code)
    data = json_body(resp)
    self.assertEqual([], data)

  def test_create_a_task_and_then_get_its_details(self):
    client = app.test_client()
    # verify test pre-conditions
    resp = client.get("/tasks/")
    data = json_body(resp)
    self.assertEqual([], data)
    # create new task
    new_task = {
      "summary": "Get milk.",
      "description": "One gallon organic whole milk."
    }
    resp = client.post(
      "/tasks/",
      data=json.dumps(new_task))
    self.assertEqual(201, resp.status_code)
    data = json_body(resp)
    self.assertIn("id", data)
    # get task details
    task_id = data["id"]
    resp = client.get(f"/tasks/{task_id:d}/")
    self.assertEqual(200, resp.status_code)
    task = json_body(resp)
    self.assertEqual(task_id, task["id"])
    self.assertEqual("Get milk.", task["summary"])
    self.assertEqual("One gallon organic whole milk.", task["description"])


