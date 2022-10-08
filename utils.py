import json


def load_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def user_object_to_dict(obj):
    return {
        "id": obj.id,
        "first_name": obj.first_name,
        "last_name": obj.last_name,
        "age": obj.age,
        "email": obj.email,
        "role": obj.role,
        "phone": obj.phone
    }


def order_object_to_dict(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "description": obj.description,
        "start_date": obj.start_date,
        "end_date": obj.end_date,
        "address": obj.address,
        "price": obj.price,
        "customer": obj.customer_id,
        "executor": obj.executor_id
    }


def offer_object_to_dict(obj):
    return {
        "id": obj.id,
        "order_id": obj.order_id,
        "executor_id": obj.executor_id
    }


