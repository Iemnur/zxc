import requests


def rq_get(url, params=None):
    res = requests.get(url, params)
    return res.json()
