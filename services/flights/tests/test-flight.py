import requests
from multiprocessing import Process
import time
import app as flights_app

def run_app():
    flights_app.app.run(port=5006)

def test_list_flights():
    p = Process(target=run_app)
    p.start()
    time.sleep(1)
    res = requests.get('http://localhost:5006/api/flights')
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    p.terminate()
