from .item_models import db as db_item
from .user_models import db as db_user


def init_app(app):
    db_user.init_app(app)
    db_item.init_app(app)
