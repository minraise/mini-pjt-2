import time, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

def fetch(session, url, params, sleep=0.3):
    try:
        ...
    except Exception as e:
        logging.error(f"요청 실패: ...")
        raise

def make_session(retries=3, backoff=0.5):
    s = requests.Session()
    retry = Retry(total=retries, backoff_factor=backoff,
                  status_forcelist=[429, 500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

def fetch(session, url, params, sleep=0.3):
    r = session.get(url, params=params, timeout=10)
    r.raise_for_status()
    time.sleep(sleep)
    return r.json()