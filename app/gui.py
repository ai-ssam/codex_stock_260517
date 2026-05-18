import tkinter as tk
from tkinter import simpledialog


def prompt_api_credentials() -> tuple[str, str]:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    app_key = simpledialog.askstring("Kiwoom API", "앱키(appkey)를 입력하세요:", parent=root)
    secret_key = simpledialog.askstring(
        "Kiwoom API", "시크릿키(secretkey)를 입력하세요:", parent=root, show="*"
    )

    root.destroy()

    if not app_key or not secret_key:
        raise ValueError("앱키/시크릿키 입력이 필요합니다.")

    return app_key.strip(), secret_key.strip()
