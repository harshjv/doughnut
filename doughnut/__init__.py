import os
import uuid
from flask import Flask
from doughnut.frontend.controllers import frontend

app = Flask(__name__)

app.register_blueprint(frontend, url_prefix='/')
