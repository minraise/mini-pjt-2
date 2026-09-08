import logging, os

os.makedirs('data/logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('data/logs/collect.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

from collector.sources.resident_pop import fetch_all
from collector.transform import transform
from collector.loader import load

def main():
    rows = fetch_all()
    resident_rows, region_rows = transform(rows)
    load(resident_rows, region_rows)

if __name__ == "__main__":
    main()