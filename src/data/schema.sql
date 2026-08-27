-- Schema

CREATE TABLE IF NOT EXISTS item_categories(
    category_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rarities(
    rarity_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS weapons(
    weapon_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    weapon_class VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS exteriors(
    exterior_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    sort_order SMALLINT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS item_collections (
    collection_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sources (
    source_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS items (
    item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    market_hash_name VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    category_id INTEGER NOT NULL
        REFERENCES item_categories(category_id),
    rarity_id INTEGER
        REFERENCES rarities(rarity_id),
    is_stattrak BOOLEAN NOT NULL DEFAULT FALSE,
    is_souvenir BOOLEAN NOT NULL DEFAULT FALSE,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS skin_details (
    item_id BIGINT PRIMARY KEY
        REFERENCES items(item_id)
        ON DELETE CASCADE,

    weapon_id INTEGER
        REFERENCES weapons(weapon_id),

    skin_name VARCHAR(150),

    exterior_id INTEGER
        REFERENCES exteriors(exterior_id),

    collection_id INTEGER
        REFERENCES item_collections(collection_id)
);

CREATE TABLE IF NOT EXISTS runs (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id INTEGER NOT NULL
        REFERENCES sources(source_id),
    currency CHAR(3) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'running'
        CHECK (
            status IN (
                'running',
                'success',
                'partial',
                'failed'
            )
        ),
    items_received INTEGER NOT NULL DEFAULT 0
        CHECK (items_received >= 0),
    items_inserted INTEGER NOT NULL DEFAULT 0
        CHECK (items_inserted >= 0),
    items_failed INTEGER NOT NULL DEFAULT 0
        CHECK (items_failed >= 0),
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS item_prices (
    price_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id BIGINT NOT NULL
        REFERENCES items(item_id),
    run_id BIGINT NOT NULL
        REFERENCES runs(run_id),
    min_price NUMERIC(14, 2),
    max_price NUMERIC(14, 2),
    mean_price NUMERIC(14, 2),
    median_price NUMERIC(14, 2),
    suggested_price NUMERIC(14, 2),
    quantity INTEGER,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (min_price IS NULL OR min_price >= 0),
    CHECK (max_price IS NULL OR max_price >= 0),
    CHECK (mean_price IS NULL OR mean_price >= 0),
    CHECK (median_price IS NULL OR median_price >= 0),
    CHECK (
        suggested_price IS NULL
        OR suggested_price >= 0
    ),
    CHECK (
        quantity IS NULL
        OR quantity >= 0
    ),
    CHECK (
        min_price IS NULL
        OR max_price IS NULL
        OR min_price <= max_price
    ),
    -- Prevent accidentally inserting the same item
    -- twice during one collection run.
    UNIQUE (item_id, run_id)
);

-- Indexes

-- for getting one item's price history
CREATE INDEX IF NOT EXISTS idx_item_prices_item_time
ON item_prices (item_id, observed_at DESC);

-- for date-based EDA
CREATE INDEX IF NOT EXISTS idx_item_prices_observed_at
ON item_prices (observed_at DESC);

-- for filtering items by category
CREATE INDEX IF NOT EXISTS idx_items_category
ON items (category_id);

-- for rarity analysis
CREATE INDEX IF NOT EXISTS idx_items_rarity
ON items (rarity_id);

-- for analyzing prices by weapon
CREATE INDEX IF NOT EXISTS idx_skin_details_weapon
ON skin_details (weapon_id);

-- for analyzing collections
CREATE INDEX IF NOT EXISTS idx_skin_details_collection
ON skin_details (collection_id);

-- for wear / exterior analysis
CREATE INDEX IF NOT EXISTS idx_skin_details_exterior
ON skin_details (exterior_id);

-- for viewing collection history by source
CREATE INDEX IF NOT EXISTS idx_runs_source_time
ON runs (source_id, started_at DESC);