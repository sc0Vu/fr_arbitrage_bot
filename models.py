from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Numeric, Enum
)
from datetime import datetime
from app import db

class Signal(db.Model):
    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    buy_price = Column(Numeric)
    sell_price = Column(Numeric)
    estimated_fee = Column(Float)
    # spread_pct = Column(Float)
    open_intrest = Column(Numeric)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    side = Column(Enum('buy', 'sell', name='order_side'))
    status = Column(String) # TODO: use enum types 
    quantity = Column(Numeric)
    leverage = Column(Numeric)
    price = Column(Numeric)
    fee = Column(Float)
    spot_hedged_order = Column(Numeric)
    signal_reason = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)