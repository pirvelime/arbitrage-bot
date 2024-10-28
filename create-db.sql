-- Drop existing table if needed (comment out if you want to preserve data)
DROP TABLE IF EXISTS market_data;

-- Create the enhanced market data table
CREATE TABLE IF NOT EXISTS market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token VARCHAR(50) NOT NULL,           -- Token/Symbol name (e.g., BTC)
    symbol VARCHAR(50) NOT NULL,          -- Trading symbol (e.g., BTC-USD)
    slug VARCHAR(100) NOT NULL,           -- URL-friendly name (e.g., bitcoin)
    link VARCHAR(255),                    -- External reference link
    exchange VARCHAR(50) NOT NULL,        -- Exchange name
    price VARCHAR(50) NOT NULL,           -- Price as string to preserve exact representation
    volume DECIMAL(20,2) NOT NULL,        -- Trading volume
    date DATETIME NOT NULL,               -- Timestamp of the data point
    
    -- Add indexes for better query performance
    CONSTRAINT market_data_unique UNIQUE (symbol, exchange, date)
);

-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_market_data_token ON market_data(token);
CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol);
CREATE INDEX IF NOT EXISTS idx_market_data_slug ON market_data(slug);
CREATE INDEX IF NOT EXISTS idx_market_data_date ON market_data(date);
CREATE INDEX IF NOT EXISTS idx_market_data_exchange ON market_data(exchange);

