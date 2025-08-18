import requests
from multiprocessing import Process
import time
import app as gateway_app

def run_app():
    gateway_app.app.run(port=5005)

def test_healthz():
    p = Process(target=run_app)
    p.start()
    time.sleep(1)
    res = requests.get('http://localhost:5005/healthz')
    assert res.status_code == 200
    p.terminate()
