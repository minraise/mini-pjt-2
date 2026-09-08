-- 마트 계층
CREATE TABLE mart_region_monthly (
    region_code       TEXT,
    base_ym           TEXT,
    avg_daily_pop     REAL,     
    weekday_pop       REAL,     
    weekend_pop       REAL,     
    peak_hour         INTEGER,  
    resident_pop      INTEGER,  
    store_count       INTEGER,   
    activity_ratio    REAL,     
    pop_per_store     REAL,     
    PRIMARY KEY (region_code, base_ym)
);

CREATE TABLE mart_hourly_heatmap (
    region_code   TEXT,     
    day_of_week   INTEGER,
    hour          INTEGER,
    avg_pop       REAL,
    PRIMARY KEY (region_code, day_of_week, hour)
);

CREATE TABLE mart_age_profile (
    region_code   TEXT,
    age_band      TEXT,     
    gender        TEXT,      
    avg_pop       REAL,      
    PRIMARY KEY (region_code, age_band, gender)
);

-- 원본 계층
CREATE TABLE flow_pop_raw (
    region_code   TEXT,
    base_date     TEXT,
    hour          INTEGER,
    total_pop     REAL,
    male_0_9      REAL,
    male_10_14    REAL,

    female_70_over REAL,
    PRIMARY KEY (region_code, base_date, hour)
);

CREATE INDEX idx_flow_region_date ON flow_pop_raw(region_code, base_date);

CREATE TABLE resident_pop (
    region_code   TEXT,
    base_ym       TEXT,
    total_pop     INTEGER,
    hh_cnt        INTEGER,
    PRIMARY KEY (region_code, base_ym)
);

CREATE TABLE store (
     store_id      TEXT,
     region_code   TEXT,
     category_m    TEXT,
     PRIMARY KEY (store_id) 
);
CREATE INDEX idx_store_region ON store(region_code);

CREATE TABLE region (
    region_code   TEXT PRIMARY KEY,
    sido_name     TEXT,
    sigungu_name  TEXT,
    dong_name     TEXT
);