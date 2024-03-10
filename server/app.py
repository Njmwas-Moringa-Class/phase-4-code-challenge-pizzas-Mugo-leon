import os
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate
from flask import Flask, request
from flask_restful import Api, Resource

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Add API instantiation
api = Api(app)

# Add serialization rules
class RestaurantResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict() for r in restaurants]

class SingleRestaurantResource(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            return restaurant.to_dict(include_pizzas=True)
        else:
            return {"error": "Restaurant not found"}, 404

    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            # Delete associated RestaurantPizzas
            RestaurantPizza.query.filter_by(restaurant_id=restaurant.id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "Restaurant not found"}, 404

# Add routes
api.add_resource(RestaurantResource, '/restaurants')
api.add_resource(SingleRestaurantResource, '/restaurants/<int:restaurant_id>')

class PizzaResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict() for p in pizzas]

api.add_resource(PizzaResource, '/pizzas')

class RestaurantPizzaResource(Resource):
    def get(self):
        # Handle GET requests
        pizzas = RestaurantPizza.query.all()
        return [rp.to_dict() for rp in pizzas]

    def post(self):
        # Handle POST requests
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")
        pizza_id = data.get("pizza_id")

        # Check if Restaurant and Pizza exist
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if not restaurant or not pizza:
            return {"errors": ["Restaurant or Pizza not found"]}, 404

        try:
            restaurant_pizza = RestaurantPizza(**data)
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(), 201
        except ValueError as e:
            return {"errors": [str(e)]}, 400
        except IntegrityError:
            return {"errors": ["validation errors"]}, 400


api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
