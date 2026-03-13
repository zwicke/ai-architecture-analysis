PRICING = {
    "gpt-4o": 0.005,
    "claude-sonnet": 0.003,
    "gemini-pro": 0.002,
    "gpt-4o-mini": 0.00015, 
    "gemini-1.5-flash": 0.000075 
    }

DEFAULT_PRICE = 0.0025


def price_per_1k(model: str) -> float:
    return PRICING.get(model, DEFAULT_PRICE)


def estimate_cost_for_row(row) -> float:
    model = row.get('model')
    price = price_per_1k(model)
    tokens = (row.get('input_tokens', 0) or 0) + (row.get('output_tokens', 0) or 0)
    return (tokens / 1000.0) * price


def estimate_total_cost(df) -> float:
    return float(df.apply(estimate_cost_for_row, axis=1).sum())


def estimate_optimized_cost(df, strategy="mid_tier") -> float:
    def row_cost(row):
        model = row.get('model')
        price = price_per_1k(model)
        if model in ("gpt-4o","gpt-4") and strategy == "mid_tier":
            price = PRICING.get('gemini-pro', price)
        tokens = (row.get('input_tokens', 0) or 0) + (row.get('output_tokens', 0) or 0)
        return (tokens / 1000.0) * price
    return float(df.apply(row_cost, axis=1).sum())
