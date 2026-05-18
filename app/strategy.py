from typing import Literal


Signal = Literal["buy", "sell", "hold"]


def simple_threshold_signal(current_price: int, threshold: int = 70000) -> Signal:
    if current_price < threshold:
        return "buy"
    if current_price > threshold * 1.05:
        return "sell"
    return "hold"
