from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, BooleanField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from wtforms.fields.html5 import DateField
from market.models.user_models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        pass

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email-address.')

    first_name = StringField(validators=[Length(min=2, max=30), DataRequired()])
    last_name = StringField(validators=[Length(min=2, max=30), DataRequired()])
    birth = DateField(validators=[DataRequired()])
    email = StringField(label='E-mail Address:', validators=[Email(), DataRequired()])
    phone_number = StringField(validators=[Length(min=10), DataRequired()])
    password_1 = PasswordField(validators=[Length(min=6), DataRequired()])
    password_2 = PasswordField(validators=[EqualTo('password_1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='E-mail Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class AddJewelryForm(FlaskForm):
    name = StringField(label='Name of Jewelry:', validators=[Length(min=10, max=100), DataRequired()])
    short_description = StringField(label='Short Description:', validators=[Length(min=10, max=200), DataRequired()])
    full_description = TextAreaField(label='Full Description:', validators=[Length(min=10, max=1000), DataRequired()])
    price = IntegerField(label='Price:', validators=[Length(min=1, max=10), DataRequired()])
    weight = FloatField(label='Weight:', validators=[Length(min=1, max=10), DataRequired()])
    is_on_discount = BooleanField(label='On Discount?')
    discount = IntegerField(label='Discount:', validators=[Length(min=1, max=10)])
    is_available = BooleanField(label='Is Available?')
    category_id = IntegerField(label='Category ID:', validators=[Length(min=1, max=10), DataRequired()])
    submit = SubmitField(label='Add!')
