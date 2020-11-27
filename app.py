from flask import Flask
from config import  app_config
from utils.scheduler import scheduler


from addons.auth.api.auth import AuthResource
from addons.image.api.image import ImageResource
from addons.public.api.public import PublicResource
from addons.profile.api.profile import ProfileResource
from addons.listing.api.listing import ListingResource
from addons.textbook.api.textbook import TextbookResource
from addons.home.api.home import HomeResource


from common.models import image
from addons.user.model import user
from addons.profile.models.profile import Profile
from addons.listing.model.listing import Listing

from addons.user.crontab import recover_unlock_chance_task




app = Flask(__name__, template_folder="static/html")

app.config.from_mapping(app_config)
scheduler.start()

AuthResource().api_register(app)
ImageResource().api_register(app)
PublicResource().api_register(app)
ProfileResource().api_register(app)
HomeResource().api_register(app)
ListingResource().api_register(app)
TextbookResource().api_register(app)


user.User.create_table()
image.Image.create_table()
Profile.create_table()
Listing.create_table()


recover_unlock_chance_task.RecoverUnlockChanceTask().schedule()



