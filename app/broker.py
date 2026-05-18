import time
from typing import Any
import requests


class KiwoomBroker:
    def __init__(self, base_url: str, app_key: str, app_secret: str, account_no: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.app_key = app_key
        self.app_secret = app_secret
        self.account_no = account_no
        self._access_token = ""
        self._token_expiry = 0.0

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}",
        }

    def authenticate(self) -> None:
        url = f"{self.base_url}/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret,
        }
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()
        self._access_token = data.get("token", "")
        self._token_expiry = time.time() + int(data.get("expires_in", 3500))
        if not self._access_token:
            raise RuntimeError(f"토큰 발급 실패: {data}")

    def ensure_token(self) -> None:
        if not self._access_token or time.time() >= self._token_expiry - 60:
            self.authenticate()

    def get_price(self, symbol: str) -> dict[str, Any]:
        self.ensure_token()
        url = f"{self.base_url}/api/dostk/stkinfo"
        params = {"stk_cd": symbol}
        res = requests.get(url, headers=self._headers(), params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_balance(self) -> dict[str, Any]:
        self.ensure_token()
        url = f"{self.base_url}/api/dostk/acnt"
        params = {"acnt_no": self.account_no}
        res = requests.get(url, headers=self._headers(), params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def place_order(self, symbol: str, qty: int, side: str) -> dict[str, Any]:
        self.ensure_token()
        url = f"{self.base_url}/api/dostk/ordr"
        payload = {
            "acnt_no": self.account_no,
            "stk_cd": symbol,
            "ordr_qty": qty,
            "sll_buy_dvsn_cd": "02" if side == "buy" else "01",
            "ordr_prc": 0,
            "ordr_dvsn_cd": "01",
        }
        res = requests.post(url, headers=self._headers(), json=payload, timeout=10)
        res.raise_for_status()
        return res.json()
