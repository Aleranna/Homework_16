import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import prettytable
from utils import load_data, user_object_to_dict, order_object_to_dict, offer_object_to_dict

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENSURE_ASCII'] = False
db: SQLAlchemy = SQLAlchemy(app)


with app.app_context():
    db.init_app(app)


    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String)
        last_name = db.Column(db.String)
        age = db.Column(db.Integer)
        email = db.Column(db.String)
        role = db.Column(db.String)
        phone = db.Column(db.String)


    class Order(db.Model):
        __tablename__ = 'order'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        description = db.Column(db.String)
        start_date = db.Column(db.String)
        end_date = db.Column(db.String)
        address = db.Column(db.String)
        price = db.Column(db.Integer)
        customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        executor = db.relationship('User', foreign_keys=[executor_id])
        customer = db.relationship('User', foreign_keys=[customer_id])

    class Offer(db.Model):
        __tablename__ = 'offer'
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        executor = db.relationship('User')
        order = db.relationship('Order')


    db.create_all()
    with db.session.begin():

        for i in load_data('users.json'):
            db.session.add(User(id=i['id'], first_name=i['first_name'], last_name=i['last_name'], age=i['age'], email=i['email'], role=i['role'], phone=i['phone']))
        for i in load_data('orders.json'):
            db.session.add(Order(id=i['id'], name=i['name'], description=i['description'], start_date=i['start_date'], end_date=i['end_date'], address=i['address'], price=i['price'], customer_id=i['customer_id'], executor_id=i['executor_id']))
        for i in load_data('offers.json'):
            db.session.add(Offer(id=i['id'], order_id=i['order_id'], executor_id=i['executor_id']))

    with db.session.begin():

        session = db.session()
        cursor = session.execute(f"SELECT * from 'offer'").cursor
        mytable = prettytable.from_db_cursor(cursor)
        mytable.max_width = 30


        @app.route('/users', methods=['GET', 'POST'])
        def get_all_users():
            if request.method == 'GET':
                users = []
                for item in User.query.all():
                    users.append(user_object_to_dict(item))
                return jsonify(users)
            if request.method == 'POST':
                data = request.json
                user = User(
                    id=data.get('id'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    age=data.get('age'),
                    email=data.get('email'),
                    role=data.get('role'),
                    phone=data.get('phone')
                )

                db.session.add(user)
                db.session.commit()
                return jsonify(user_object_to_dict(user))


        @app.route('/users/<pk>', methods=['GET', 'PUT', 'DELETE'])
        def get_one_user(pk):
            if request.method == 'GET':
                user = User.query.get(pk)
                return jsonify(user_object_to_dict(user))
            if request.method == 'PUT':
                data = request.json
                user = User.query.get(pk)
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.age = data.get('age')
                user.email = data.get('email')
                user.role = data.get('role')
                user.phone = data.get('phone')
                db.session.add(user)
                db.session.commit()
                return jsonify(user_object_to_dict(user))
            if request.method == 'DELETE':
                user = User.query.get(pk)
                db.session.delete(user)
                db.session.commit()
                return 'User deleted'


        @app.route('/orders', methods=['GET', 'POST'])
        def get_all_orders():
            if request.method == 'GET':
                orders = []
                for item in Order.query.all():
                    orders.append(order_object_to_dict(item))
                return json.dumps(orders, indent=10, ensure_ascii=False)
            if request.method == 'POST':
                data = request.json
                order = Order(
                    id=data.get('id'),
                    name=data.get('name'),
                    description=data.get('description'),
                    start_date=data.get('start_date'),
                    end_date=data.get('end_date'),
                    address=data.get('address'),
                    price=data.get('price'),
                    customer_id=data.get('customer_id'),
                    executor_id=data.get('executor_id')
                )
                db.session.add(order)
                db.session.commit()
                return 'order added'


        @app.route('/orders/<pk>', methods=['GET', 'PUT', 'DELETE'])
        def get_one_order(pk):
            if request.method == 'GET':
                order = Order.query.get(pk)
                return json.dumps(order_object_to_dict(order), indent=4, ensure_ascii=False)
            if request.method == 'PUT':
                data = request.json
                order = Order.query.get(pk)
                order.name = data.get('name')
                order.description = data.get('description')
                order.start_date = data.get('start_date')
                order.end_date = data.get('end_date')
                order.address = data.get('address')
                order.price = data.get('price')
                order.customer_id = data.get('customer_id')
                order.executor_id = data.get('executor_id')

                db.session.add(order)
                db.session.commit()
                return 'order updated'
            if request.method == 'DELETE':
                order = Order.query.get(pk)
                db.session.delete(order)
                db.session.commit()
                return 'Order deleted'


        @app.route('/offers', methods=['GET', 'POST'])
        def get_all_offers():
            if request.method == 'GET':
                offers = []
                for item in Offer.query.all():
                    offers.append(offer_object_to_dict(item))
                return jsonify(offers)
            if request.method == 'POST':
                data = request.json
                offer = Offer(
                    id=data.get(''),
                    order_id=data.get(''),
                    executor_id=data.get('')
                )
                db.session.add(offer)
                db.session.commit()
                return 'offer added'


        @app.route('/offers/<pk>', methods=['GET', 'PUT', 'DELETE'])
        def get_one_offer(pk):
            if request.method == 'GET':
                offer = Offer.query.get(pk)
                return jsonify(offer_object_to_dict(offer))
            if request.method == 'PUT':
                data = request.json
                offer = Offer.query.get(pk)
                offer.id = data.get('id')
                offer.order_id = data.get('order_id')
                offer.executor_id = data.get('executor_id')
                return 'offer updated'
            if request.method == 'DELETE':
                offer = Offer.query.get(pk)
                db.session.delete(offer)
                db.session.commit()
                return 'offer deleted'



        if __name__ == "__main__":
            app.run()






