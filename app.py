import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from models import db, Item

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/items")
def list_items():
    return jsonify([i.to_dict() for i in Item.query.all()])


@app.post("/items")
def create_item():
    data = request.get_json()
    item = Item(name=data["name"], description=data.get("description"))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = db.get_or_404(Item, item_id)
    return jsonify(item.to_dict())


@app.put("/items/<int:item_id>")
def update_item(item_id):
    item = db.get_or_404(Item, item_id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify(item.to_dict())


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    item = db.get_or_404(Item, item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"deleted": item_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
