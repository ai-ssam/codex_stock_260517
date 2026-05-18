from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_key: str
    app_secret: str
    account_no: str
    env: str
    base_url_mock: str
    base_url_live: str
    target_symbol: str
    order_quantity: int
    max_position_value: int
    max_daily_loss: int

    @property
    def is_live(self) -> bool:
        return self.env.lower() == "live"

    @property
    def base_url(self) -> str:
        return self.base_url_live if self.is_live else self.base_url_mock


def load_settings() -> Settings:
    return Settings(
        app_key=os.getenv("KIWOOM_APP_KEY", ""),
        app_secret=os.getenv("KIWOOM_APP_SECRET", ""),
        account_no=os.getenv("KIWOOM_ACCOUNT_NO", ""),
        env=os.getenv("KIWOOM_ENV", "mock"),
        base_url_mock=os.getenv("KIWOOM_BASE_URL_MOCK", "https://openapi.kiwoom.com"),
        base_url_live=os.getenv("KIWOOM_BASE_URL_LIVE", "https://openapi.kiwoom.com"),
        target_symbol=os.getenv("TARGET_SYMBOL", "005930"),
        order_quantity=int(os.getenv("ORDER_QUANTITY", "1")),
        max_position_value=int(os.getenv("MAX_POSITION_VALUE", "500000")),
        max_daily_loss=int(os.getenv("MAX_DAILY_LOSS", "30000")),
    )
