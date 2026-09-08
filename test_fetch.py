from collector.client import make_session
from collector.sources.resident_pop import fetch_one

session = make_session()
rows = fetch_one(session, "1111000000", "202605")
print(len(rows))
print(rows[0])