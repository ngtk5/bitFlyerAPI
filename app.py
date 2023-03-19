import threading
import tkinter as tk
from tkinter import ttk
from bitflyer_api import BitFlyerAPI
from create_file import db_to_excel_file
from functools import partial


class MyApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("BitFlyer仮想通貨価格調査App")  # タイトル
        self.master.geometry("400x120")  # ウィンドウサイズ
        self.bf_api = BitFlyerAPI()
        self.button_list = []
        self.under_symbol_list = [symbol.replace('/', '_') for symbol in self.bf_api.available_symbols]
        self.create_widget()

    def create_widget(self) -> None:
        """ 各ウィジェットを生成・配置する """
        fetch_button = tk.Button(
            text="価格を調べる",
            width=10,
            command=self.run_fetch_symbols_info
        )
        self.insert_button_list(fetch_button)
        fetch_button.grid(row=0, column=0)

        row = 1
        column = 0
        for slash_symbol, under_symbol in zip(self.bf_api.available_symbols, self.under_symbol_list):
            button_ = tk.Button(
                text=slash_symbol,
                width=10,
                command=partial(self.run_db_to_excel_file, under_symbol)
            )
            self.insert_button_list(button_)
            button_.grid(row=row, column=column)

            column += 1
            if column >= 5:
                row += 1
                column = 0

    def run_db_to_excel_file(self, under_symbol):
        progress_window = ProgressBarWindow(self.master)
        t = threading.Thread(target=db_to_excel_file(under_symbol))
        t.start()
        self.disable_buttons()
        while t.is_alive():
            progress_window.start()
            self.master.update()
        progress_window.stop()
        self.enable_buttons()

    def insert_button_list(self, button) -> None:
        self.button_list.append(button)

    def run_fetch_symbols_info(self) -> None:
        progress_window = ProgressBarWindow(self.master)
        t = threading.Thread(target=self.bf_api.fetch_symbols_info)
        t.start()
        self.disable_buttons()
        while t.is_alive():
            progress_window.start()
            self.master.update()
        progress_window.stop()
        self.enable_buttons()

    def disable_buttons(self) -> None:
        for button in self.button_list:
            button.config(state="disabled")  # ボタンを無効にする

    def enable_buttons(self) -> None:
        for button in self.button_list:
            button.config(state="normal")  # ボタンを有効に戻す


class ProgressBarWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("実行中...")
        self.top.geometry("300x50")

        self.progressbar = ttk.Progressbar(self.top, mode="indeterminate", length=280)
        self.progressbar.pack(pady=10)
        # プログレスウィンドウをモーダルウィンドウとして表示
        self.top.grab_set()

    def start(self) -> None:
        self.progressbar.start(interval=10)

    def stop(self) -> None:
        self.progressbar.stop()
        self.top.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    root.mainloop()
