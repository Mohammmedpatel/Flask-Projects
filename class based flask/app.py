from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///items.db'

db = SQLAlchemy(app)             
ma = Marshmallow(app)            
api = Api(app)                   


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        fields = ("id", "name", "description")

with app.app_context():
    db.create_all()

class ItemListView(Resource):

    # Add a new item
    def post(self):
        item = ItemSchema().load(request.get_json())

        new_item = Item(**item)
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({"message": "Item added"})

    def get(self):
        items = Item.query.all()
        return ItemSchema(many=True).dump(items)


class ItemView(Resource):
    def get(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404
        return ItemSchema().dump(item)

    def put(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        update_item = ItemSchema().load(request.get_json())
        item.name = update_item.get("name", item.name)
        item.description = update_item.get("description", item.description)

        db.session.commit()
        return jsonify({"message": "Item updated"})

    def delete(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"})


api.add_resource(ItemListView, "/items")
api.add_resource(ItemView, "/items/<int:item_id>")

if __name__ == "__main__":
    app.run(debug=True)