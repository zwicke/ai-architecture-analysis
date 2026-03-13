MARKET_BENCHMARKS = {
    "high_tier": {"best_market_price": 0.003},
    "low_tier": {"best_market_price": 0.000075}
}

def calculate_arbitrage_opportunity(df):
    current_total = df.apply(lambda row: (row['input_tokens'] + row['output_tokens'])/1000 * 0.005, axis=1).sum()
    best_market_total = df.apply(lambda row: (row['input_tokens'] + row['output_tokens'])/1000 * 0.003, axis=1).sum()
    return max(0.0, current_total - best_market_total)