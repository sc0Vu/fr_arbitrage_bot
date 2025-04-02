from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Order
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "YOUR_DATABASE_URL")

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "symbol": o.symbol, "price": o.price} for o in orders])

@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()

if __name__ == "__main__":
    app.run(debug=True)