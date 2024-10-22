#!/usr/bin/env python3
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakeries_data = []
    
    for bakery in all_bakeries:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at) if bakery.updated_at else None,
            'baked_goods': []
        }
        
        for good in bakery.baked_goods:
            good_dict = {
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'bakery_id': good.bakery_id,
                'created_at': str(good.created_at),
                'updated_at': str(good.updated_at) if good.updated_at else None
            }
            bakery_dict['baked_goods'].append(good_dict)
            
        bakeries_data.append(bakery_dict)
    
    return jsonify(bakeries_data)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    
    bakery_dict = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': str(bakery.created_at),
        'updated_at': str(bakery.updated_at) if bakery.updated_at else None,
        'baked_goods': []
    }
    
    for good in bakery.baked_goods:
        good_dict = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'bakery_id': good.bakery_id,
            'created_at': str(good.created_at),
            'updated_at': str(good.updated_at) if good.updated_at else None
        }
        bakery_dict['baked_goods'].append(good_dict)
    
    return jsonify(bakery_dict)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = []
    
    for good in baked_goods:
        bakery = good.bakery
        good_dict = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'bakery_id': good.bakery_id,
            'created_at': str(good.created_at),
            'updated_at': str(good.updated_at) if good.updated_at else None,
            'bakery': {
                'id': bakery.id,
                'name': bakery.name,
                'created_at': str(bakery.created_at),
                'updated_at': str(bakery.updated_at) if bakery.updated_at else None
            } if bakery else None
        }
        baked_goods_data.append(good_dict)
    
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not baked_good:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)
    
    bakery = baked_good.bakery
    baked_good_data = {
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price,
        'bakery_id': baked_good.bakery_id,
        'created_at': str(baked_good.created_at),
        'updated_at': str(baked_good.updated_at) if baked_good.updated_at else None,
        'bakery': {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at) if bakery.updated_at else None
        } if bakery else None
    }
    
    return jsonify(baked_good_data)

if __name__ == '__main__':
    app.run(port=5555, debug=True)