def check_position_limit(current_price: int, qty: int, max_position_value: int) -> bool:
    return current_price * qty <= max_position_value
