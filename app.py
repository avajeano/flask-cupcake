from flask import Flask, request, jsonify, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
# print all SQL statements to the terminal - helpful for debugging
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)

@app.route('/', methods=["GET", "POST"])
def index_page():
    

    form = AddCupcakeForm()

    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data
        cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        db.session.add(cupcake)
        db.session.commit()
        return redirect('/')
    else:
        cupcakes = Cupcake.query.all()
        return render_template('index.html', cupcakes = cupcakes, form=form)

@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""
    new_cupcake = Cupcake(flavor = request.json["flavor"], size = request.json["size"], rating = request.json["rating"], image = request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()

    # specified status code 201
    return (jsonify(cupcake = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request."""
    cupcake = Cupcake.query.get_or_404(id)

    # changes the data or keeps it as is
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake with the id passed in the URL."""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(msg = "deleted")