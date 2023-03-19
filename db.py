import sqlite3


class SQLiteDB:
    def __init__(self, dbname: str):
        """
        SQLiteDBクラスのコンストラクタ
        Args:
            dbname (str): データベースのファイル名
        """
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def create_table(self, query: str) -> None:
        """
        テーブルを作成する
        Args:
            query (str): テーブルを作成するSQLクエリ
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, query: str, data: tuple) -> None:
        """
        データを挿入する
        Args:
            query (str): データを挿入するSQLクエリ
            data (tuple): 挿入するデータのタプル
        """
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
        # テーブル内に同じデータがあれば挿入せずに次の処理へ
        except sqlite3.IntegrityError:
            pass

    def fetch_data(self, query: str) -> list:
        """
        データを取得する
        Args:
            query (str): データを取得するSQLクエリ
        Returns:
            list: 取得したデータのリスト
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def close(self) -> None:
        """ データベースの接続を閉じる """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    pass
