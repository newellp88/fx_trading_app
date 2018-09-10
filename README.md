
# About

An implementation of three very basic trading strategies. One uses the Ichimoku indicator, one is a moving average crossover, and the third trades on simple signals from Heikin candles.

The program is meant to be run with three different Oanda accounts, per their API restrictions. To run this you will need account IDs and API tokens.

# Current usage

Install and activate RabbitMQ, then cd into the *oanda* folder and execute run.py in terminal. This will execute the Celery app, running the main functions on 5 minute loops.

# To-do

Tighten up the Flask and HTML for the visualization part of the app. Memory optimization: RAM usage hovers around 6 GB at all times.


