import os
import sys

sys.path.append("../")

from mofeapi.client import Client

if __name__ == "__main__":
    client = Client()
    client.login(
        os.environ["MOFE_USERNAME"], os.environ["MOFE_PASSWORD"]
    )  # OS の 環境変数からユーザー名とパスワードを取得
    contests, creating_problems, posts = client.top()  # トップページからコンテストの情報を取得する
    for contest in contests:
        print(contest.name)  # コンテストの名前を表示する

# 実行結果:
# $ python3 get_contest.py
# TUATPC 2025 Spring
# TeraCoder2024
# TSG LIVE! 13 プログラミングコンテスト
# 筑波大学プログラミングコンテスト2024
# お茶大徽音祭コンテスト2024
# メルカリ競プロコンテスト2024
# ゆるふわ競技プログラミングオンサイト at FORCIA #7
# TUATPC2024Summer (Heuristic)
# TUATPC2024Summer (Algorithm)
# KSDUPC 2024
