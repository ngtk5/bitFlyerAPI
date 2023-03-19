import ccxt
from datetime import datetime
import settings
from db import SQLiteDB
import pytz


class BitFlyerAPI:
    def __init__(self):
        self.symbol_name = None  # 仮想通貨名(str)
        self.ask = None  # 価格(float)
        self.formatted_date_str = None  # 整形した日付(str)
        # bitFlyerのインスタンス作成
        self.bf = ccxt.bitflyer({
            'apiKey': settings.API_KEY,
            'secret': settings.API_SECRET_KEY
        })
        # 板情報
        self.markets = self.bf.load_markets()
        # 仮想通貨名のリスト
        self._symbols = [values["symbol"] for values in self.markets.values() if
                         ':' not in values["symbol"]]
        # 日付文字列をdatetimeオブジェクトに変換する前に、タイムゾーンを指定
        self.tz = pytz.timezone('Asia/Tokyo')  # 日本標準時（UTC+9）に設定

    def fetch_symbols_info(self) -> None:
        # SQLiteDBインスタンスの生成
        db = SQLiteDB("db/symbols_info.db")
        for symbol in self.available_symbols:
            # 板情報
            ticker = self.bf.fetch_ticker(symbol)

            self.symbol_name = ticker["info"]["product_code"]
            self.ask = ticker['ask']

            # 日付文字列をdatetimeオブジェクトに変換する
            datetime_obj = datetime.strptime(
                ticker["datetime"],
                '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                tzinfo=pytz.utc).astimezone(self.tz)

            # 指定されたフォーマットに変換する
            self.formatted_date_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            self.insert_symbols_info_to_db(db)
        # データベースを閉じる
        db.close()

    def insert_symbols_info_to_db(self, db) -> None:
        """ 仮想通貨情報を元にテーブルにデータを挿入する """
        # テーブルの作成
        db.create_table(f"""
        CREATE TABLE IF NOT EXISTS {self.symbol_name} (
            ask REAL,
            date TEXT,
            UNIQUE(ask, date)
            )""")

        # symbol情報をテーブルに挿入
        db.insert_data(
            f'INSERT INTO {self.symbol_name}( ask, date ) VALUES ( ?, ? )',
            (self.ask, self.formatted_date_str)
        )

    @property
    def available_symbols(self) -> list:
        return self._symbols


if __name__ == '__main__':
    pass
