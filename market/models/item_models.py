from market import db


class Category(db.Model):
    """
    Category Database
    """
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    jewelries = db.relationship('Jewelry', backref='category', lazy=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    category_description = db.Column(db.String(500), unique=True, nullable=False)


class Jewelry(db.Model):
    """
    Jewelry Database
    """
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    short_description = db.Column(db.String(350), nullable=False)
    full_description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Float(), nullable=False)
    is_on_discount = db.Column(db.Boolean(), default=False, nullable=False)
    discount = db.Column(db.Integer(), default=0)
    is_available = db.Column(db.Boolean(), default=True, nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=False)
