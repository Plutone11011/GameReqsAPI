CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    genre TEXT,
    developer TEXT,
    ram_min INTEGER NOT NULL,
    cpu_min TEXT NOT NULL,
    gpu_min TEXT NOT NULL,
    OS_min TEXT NOT NULL,
    storage_min INTEGER NOT NULL,
    ram_rec INTEGER,
    cpu_rec TEXT,
    gpu_rec TEXT,
    OS_rec TEXT,
    storage_rec INTEGER
);
