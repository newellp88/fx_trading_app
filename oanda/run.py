import os

os.system('celery -A oanda worker --autoscale=150,50 -B -E -l info')
