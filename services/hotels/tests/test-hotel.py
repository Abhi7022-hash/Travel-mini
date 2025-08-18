import requests
from multiprocessing import Process
import time
import app as hotels_app

def run_app():
    hotels_app.app.run(port=5007)

def test_list_hotels():
    p = Process(target=run_app)
    p.start()
    time.sleep(1)
    res = requests.get('http://localhost:5007/api/hotels')
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    p.terminate()
