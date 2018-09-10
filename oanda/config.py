import sqlite3
from celery import Celery

conn = sqlite3.connect('db/trading.db')

trading_app = Celery('oanda', backend='rpc://', broker='amqp://localhost')
