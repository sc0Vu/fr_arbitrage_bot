from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Order
import os
import ccxt.pro as ccxt
import asyncio
import threading
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "YOUR_DATABASE_URL")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "YOUR_BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET", "YOUR_BINANCE_SECRET")
PAIRS = os.getenv("PAIRS", "YOUR_PAIRS")

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_api_provider():
    exchange = ccxt.binance({
        'apiKey': BINANCE_API_KEY,
        'secret': BINANCE_SECRET,
    })
    return exchange

binance = init_api_provider()
symbols = PAIRS.split(',')

job_queue = asyncio.Queue()
job_results = {}

async def job_scheduler():
    while True:
        job_id, fn = await job_queue.get()
        result = False
        if asyncio.iscoroutine(fn):
            result = await fn

        job_results[job_id] = result
        job_queue.task_done()
        print(f"[{job_id}] Done.")

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "symbol": o.symbol, "price": o.price} for o in orders])

@app.route("/fetch_frs", methods=["GET"])
def fetch_frs():
    job_id = str(uuid.uuid4())
    asyncio.run_coroutine_threadsafe(job_queue.put((job_id, binance.fetch_funding_rates(symbols))), asyncio_loop)
    return jsonify({"id": job_id})

@app.route("/frs/<job_id>", methods=["GET"])
def frs(job_id):
    result = job_results.get(job_id, "Not found")
    return jsonify({"id": job_id, "result": result})

@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    asyncio_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(asyncio_loop,))
    t.start()

    asyncio.run_coroutine_threadsafe(job_scheduler(), asyncio_loop)

    app.run(debug=True, use_reloader=False)