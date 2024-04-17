from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image_url = "https://tinyurl.com/demo-cupcake"

def connect_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()

class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=default_image_url)

    def serialize(self):
        """Serialize cupcake to a dict of cupcake info."""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }