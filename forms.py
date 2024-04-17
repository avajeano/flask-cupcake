from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import URL 

class AddCupcakeForm(FlaskForm):
    """For for adding a cupcake."""

    flavor = StringField("Flavor")
    size = StringField("Size")
    rating = FloatField("Rating")
    image = StringField("Image URL", validators=[URL()])