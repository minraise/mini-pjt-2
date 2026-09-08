import logging
from collector.client import make_session, fetch
from collector import config


def extract_items(response: dict) -> list:
    """응답에서 item 리스트를 안전하게 꺼낸다.
    NODATA일 때 items가 빈 문자열("")로 오므로 그대로 인덱싱하면 에러."""
    items = response.get("Response", {}).get("items", "")
    if not isinstance(items, dict):      # "" 이거나 예상 밖 타입
        return []
    item = items.get("item", [])
    # 결과가 1건이면 리스트가 아니라 dict 하나로 올 수 있으니 확인 필요
    if isinstance(item, dict):
        return [item]
    return item


def fetch_one(session, sgg_code: str, ym: str) -> list:
    """자치구 1개 × 조회월 1개를 페이징까지 끝까지 수집."""
    collected = []
    page = 1

    while True:
        params = {
            "serviceKey": config.API_KEY,
            "admmCd": sgg_code,
            "srchFrYm": ym,
            "srchToYm": ym,
            "lv": config.LV,
            "type": "JSON",
            "numOfRows": config.NUM_OF_ROWS,
            "pageNo": page,
        }

        response = fetch(session, config.BASE_URL, params, sleep=config.SLEEP_SEC)
        items = extract_items(response)
        head = response.get("Response", {}).get("head", {})
        total_count = int(head.get("totalCount", 0))

        collected.extend(items)

        # ── TODO: 여기서 반복을 멈출 조건 ──
        # 1) 이번에 받은 게 없으면 (무한루프 방지)
        # 2) 지금까지 받은 개수가 total_count 이상이면
        if not items or len(collected) >= total_count:
            break

        page += 1

    logging.info(f"{config.SGG_CODES.get(sgg_code, sgg_code)} {ym} → {len(collected)}건")
    return collected


def fetch_all() -> list:
    """자치구 25개 × 조회월 전체를 수집."""
    session = make_session()
    all_rows = []

    for sgg_code in config.SGG_CODES:
        for ym in config.TARGET_YMS:
            try:
                rows = fetch_one(session, sgg_code, ym)
                all_rows.extend(rows)
            except Exception as e:
                logging.error(f"수집 실패: {sgg_code} {ym} - {e}")
                continue      # 한 건 실패해도 나머지는 계속

    logging.info(f"총 {len(all_rows)}건 수집 완료")
    return all_rows

if __name__ == "__main__":
    session = make_session()
    rows = fetch_one(session, "1111000000", "202605")
    print(len(rows))
    print(rows[0])