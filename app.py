from flask import Flask
from config import  app_config
from addons.auth.api.auth import AuthResource
from addons.image.api.image import ImageResource
from common.models import user, image
from addons.profile.models.profile import Profile


app = Flask(__name__)
app.config.from_mapping(app_config)
AuthResource().api_register(app)
ImageResource().api_register(app)
user.User.create_table()
image.Image.create_table()
Profile.create_table()


