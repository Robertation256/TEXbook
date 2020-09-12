from flask import Flask
from config import  app_config
from auth.api.auth import AuthResource

app = Flask(__name__)
app.config.from_mapping(app_config)
AuthResource().api_register(app)


