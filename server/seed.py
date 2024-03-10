#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")

    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(
        name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizza...")

    # Commit the restaurants and pizzas first to ensure they have IDs
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.commit()

    # Fetch the IDs of the created restaurants and pizzas
    shack_id = shack.id
    bistro_id = bistro.id
    palace_id = palace.id

    cheese_id = cheese.id
    pepperoni_id = pepperoni.id
    california_id = california.id

    pr1 = RestaurantPizza(restaurant_id=shack_id, pizza_id=cheese_id, price=1)
    pr2 = RestaurantPizza(restaurant_id=bistro_id, pizza_id=pepperoni_id, price=4)
    pr3 = RestaurantPizza(restaurant_id=palace_id, pizza_id=california_id, price=5)
    restaurantPizzas = [pr1, pr2, pr3]

    db.session.add_all(restaurantPizzas)
    db.session.commit()

    print("Seeding done!")
