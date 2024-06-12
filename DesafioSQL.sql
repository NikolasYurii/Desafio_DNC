CREATE TABLE Weather (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100),
    temperature FLOAT,
    humidity INT,
    timestamp TIMESTAMP
);

CREATE TABLE Traffic (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    duration INT,
    distance FLOAT,
    timestamp TIMESTAMP
);
