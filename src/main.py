import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import IntegerField, StringField, PasswordField
from wtforms.fields import BooleanField, SubmitField, URLField
from wtforms.fields import FloatField, TextAreaField


app = Flask(__name__)
app.secret_key = 'dev'
bootstrap = Bootstrap5(app)
APP_TABLE_NAME = os.environ.get('APP_TABLE_NAME', '')


class ReviewForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(1, 50)])
    product_link = URLField()
    rating = IntegerField()
    review_text = TextAreaField()
    submit = SubmitField()


reviews = [
    {'product_name': 'Foo Product', 'product_link': '', 'rating': '4.5',
     'review_text': 'This is my review of foo.'},
    {'product_name': 'Bar Product', 'product_link': '', 'rating': '4.5',
     'review_text': 'This is my review of bar.'},
    {'product_name': 'Baz Product', 'product_link': '', 'rating': '4.5',
     'review_text': 'This is my review of baz.'},
]


@app.route("/")
def index():
    return render_template(
        'index.html',
        reviews=reviews,
        table_name=APP_TABLE_NAME,
    )


@app.route("/review", methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        flash('Review added!')
        return redirect(url_for('index'))
    return render_template(
        'review.html',
        form=form,
    )


@app.route("/ping")
def ping():
    return "pong"
