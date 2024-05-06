CREATE TABLE publishers (
    publisher_id SERIAL PRIMARY KEY, 
    publisher_name TEXT UNIQUE NOT NULL 
);

CREATE TABLE clicks (
    click_id SERIAL PRIMARY KEY,
    publisher_id INTEGER REFERENCES publishers(publisher_id),
    click_timestamp TIMESTAMP NOT NULL,
    click_date DATE,
    click_time TIME,
    country_iso_code TEXT,
    city TEXT,
    os_name TEXT,
    os_version TEXT,
    browser TEXT,
    browser_version TEXT,
    device_type TEXT,
    publisher_category TEXT
);
