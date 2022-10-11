import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import IntegerField, StringField, PasswordField
from wtforms.fields import BooleanField, SubmitField, URLField
from wtforms.fields import FloatField, TextAreaField

from ddb import DDBClient, ProductReview


app = Flask(__name__)
app.config['DDB_TABLE_NAME'] = os.environ.get('APPTABLE_NAME', '')
app.secret_key = 'dev'
bootstrap = Bootstrap5(app)
ddb = DDBClient(app)


class ReviewForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(1, 50)])
    product_link = URLField()
    rating = IntegerField(validators=[DataRequired()])
    review_text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


reviews = [
    {'product_name': 'Foo Product', 'product_link': '', 'rating': 5,
     'review_text': 'This is my review of foo.'},
    {'product_name': 'Bar Product', 'product_link': '', 'rating': 5,
     'review_text': 'This is my review of bar.'},
    {'product_name': 'Baz Product', 'product_link': '', 'rating': 4,
     'review_text': 'This is my review of baz.'},
]


@app.route("/")
def index():
    reviews = ddb.get_reviews()
    return render_template(
        'index.html',
        reviews=reviews,
    )


@app.route("/review", methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = ProductReview(
            name=form.product_name.data,
            rating=form.rating.data,
            review=form.review_text.data,
            url=form.product_link.data,
        )
        ddb.create_review(new_review)
        flash('Review added!')
        return redirect(url_for('index'))
    return render_template(
        'review.html',
        form=form,
    )


@app.route("/ping")
def ping():
    return "pong"
