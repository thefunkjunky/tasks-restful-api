from flask import Flask

app = Flask(__name__)


@app.route("/tasks/")
def get_all_tasks():
  return "[]", 200


if __name__ == '__main__':
  app.run()
