from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
#lets creat a route
@app.route("/")
def hello_world():
  return "Hello Nurye How are u"
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
