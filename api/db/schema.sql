CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    developer TEXT,
    ram_min FLOAT,
    cpu_min TEXT,
    gpu_min TEXT,
    OS_min TEXT,
    storage_min FLOAT,
    ram_rec FLOAT,
    cpu_rec TEXT,
    gpu_rec TEXT,
    OS_rec TEXT,
    storage_rec FLOAT
);
