import tkinter as tk
from tkinter import simpledialog


class EnvSelectDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.title("Kiwoom 모드 선택")
        self.resizable(False, False)
        self.mode_var = tk.StringVar(value="mock")
        self.result: str | None = None

        tk.Label(self, text="실행 모드를 선택하세요").pack(padx=16, pady=(12, 8))
        tk.Radiobutton(self, text="모의투자 (mock)", variable=self.mode_var, value="mock").pack(anchor="w", padx=16)
        tk.Radiobutton(self, text="실전투자 (live)", variable=self.mode_var, value="live").pack(anchor="w", padx=16)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=12)
        tk.Button(button_frame, text="확인", width=10, command=self._on_ok).pack(side="left", padx=6)
        tk.Button(button_frame, text="취소", width=10, command=self._on_cancel).pack(side="left", padx=6)

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.grab_set()

    def _on_ok(self) -> None:
        self.result = self.mode_var.get()
        self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.destroy()


def prompt_runtime_inputs() -> tuple[str, str, str]:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    env_dialog = EnvSelectDialog(root)
    root.wait_window(env_dialog)
    env_mode = env_dialog.result

    app_key = simpledialog.askstring("Kiwoom API", "앱키(appkey)를 입력하세요:", parent=root)
    secret_key = simpledialog.askstring(
        "Kiwoom API", "시크릿키(secretkey)를 입력하세요:", parent=root, show="*"
    )

    root.destroy()

    if env_mode not in {"mock", "live"}:
        raise ValueError("실행 모드 선택이 필요합니다.")
    if not app_key or not secret_key:
        raise ValueError("앱키/시크릿키 입력이 필요합니다.")

    return env_mode, app_key.strip(), secret_key.strip()
