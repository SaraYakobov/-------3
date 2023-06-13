from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_cors import CORS
from config import DBUSER,DBHOST,DBPASS
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/postgres'
app.config['SECRET_KEY'] = 'hukjrshobnfkhsu4g2456ghkr'

db = SQLAlchemy(app)
api = Api(app)

CORS(app)

class Dish(db.Model):
    __tablename__ = 'users_dish'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    imageUrl = db.Column(db.Text)
    price = db.Column(db.Boolean)
    is_gluten_free = db.Column(db.Boolean, default=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer,db.ForeignKey('users_category.id'),nullable=False)

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "imageUrl":self.imageUrl,
            "price":self.price,
            "is_gluten_free":self.is_gluten_free,
            "is_vegetarian":self.is_vegetarian,
            "category":self.category.name
        }



class Category(db.Model):
    __tablename__ = 'users_category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    imageUrl = db.Column(db.Text)
    dishes = db.relationship('Dish', backref='category')

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "dishes":[dish.serialize() for dish in self.dishes]
        }


with app.app_context():
    db.create_all()


class CategoryAll(Resource):
    def get(self):
        categories = Category.query.all()
        return [category.serialize() for category in categories]
    

class DishAll(Resource):
    def get(self):
        dishes = Dish.query.filter_by(**request.args).all()
        return [dish.serialize() for dish in dishes][::-1]

api.add_resource(CategoryAll,'/categories')
api.add_resource(DishAll,'/dishes')

app.run(debug=True,host="0.0.0.0")