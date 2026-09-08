def transform(rows: list) -> tuple:
    """API 응답 리스트를 (resident_pop용, region용) 두 리스트로 변환."""
    resident_rows = []
    region_rows = []
    seen_codes = set()          # region은 중복 제거용

    for r in rows:
        code = r["admmCd"][:8]          # 10자리 → 8자리

        resident_rows.append((
            code,
            r["statsYm"],
            int(r["totNmprCnt"]),        # 문자열 → 정수
            int(r["hhCnt"]),                          # 세대수도 같은 방식으로
        ))

        # region은 같은 동이 여러 달 반복되니 한 번만
        if code not in seen_codes:
            region_rows.append((
                code,
                r["ctpvNm"],
                r["sggNm"],
                r["dongNm"],
            ))
            seen_codes.add(code)

    return resident_rows, region_rows