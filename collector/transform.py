def transform(rows: list) -> tuple:
    resident_rows = []
    region_rows = []
    seen_codes = set()

    for r in rows:
        code = r["admmCd"][:8]

        resident_rows.append((
            code,
            r["statsYm"][:4] + '-' + r["statsYm"][4:6],
            int(r["totNmprCnt"]), 
            int(r["hhCnt"]), 
        ))

        if code not in seen_codes:
            region_rows.append((
                code,
                r["ctpvNm"],
                r["sggNm"],
                r["dongNm"],
            ))
            seen_codes.add(code)

    return resident_rows, region_rows