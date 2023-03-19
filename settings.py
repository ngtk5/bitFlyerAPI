import os
from os.path import join, dirname
from dotenv import load_dotenv

# 参考サイト：https://qiita.com/hedgehoCrow/items/2fd56ebea463e7fc0f5b
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")  # 環境変数の値をAPI_KEYに代入
API_SECRET_KEY = os.environ.get("API_SECRET_KEY")  # 環境変数の値をAPI_SECRET_KEYに代入


if __name__ == '__main__':
    pass
