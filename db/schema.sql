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