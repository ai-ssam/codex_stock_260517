from app.config import load_settings
from app.broker import KiwoomBroker
from app.risk import check_position_limit
from app.strategy import simple_threshold_signal


def parse_price(price_response: dict) -> int:
    for key in ("cur_prc", "current_price", "price"):
        if key in price_response:
            return int(str(price_response[key]).replace(",", ""))
    raise ValueError(f"현재가 필드를 찾지 못했습니다: {price_response}")


def run_once() -> None:
    settings = load_settings()
    broker = KiwoomBroker(
        base_url=settings.base_url,
        app_key=settings.app_key,
        app_secret=settings.app_secret,
        account_no=settings.account_no,
    )

    price_raw = broker.get_price(settings.target_symbol)
    current_price = parse_price(price_raw)
    signal = simple_threshold_signal(current_price)

    print(f"[MODE={settings.env}] symbol={settings.target_symbol}, price={current_price}, signal={signal}")

    if signal in ("buy", "sell"):
        allowed = check_position_limit(current_price, settings.order_quantity, settings.max_position_value)
        if not allowed:
            print("리스크 제한으로 주문 차단")
            return

        result = broker.place_order(settings.target_symbol, settings.order_quantity, signal)
        print("주문 결과:", result)
    else:
        print("주문 없음")


if __name__ == "__main__":
    run_once()
