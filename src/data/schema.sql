
CREATE TABLE IF NOT EXISTS skin_prices (
    id SERIAL PRIMARY KEY,
    market_hash_name TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    currency TEXT NOT NULL,
    min_price NUMERIC,
    max_price NUMERIC,
    mean_price NUMERIC,
    median_price NUMERIC,
    suggested_price NUMERIC,
    quantity INTEGER,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_skin_prices_history
    ON skin_prices (id, source, fetched_at);
