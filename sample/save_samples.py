import os
import sys

sys.path.append("../")

from mofeapi.client import Client

if __name__ == "__main__":
    client = Client()
    client.login(
        os.environ["MOFE_USERNAME"], os.environ["MOFE_PASSWORD"]
    )  # OS の 環境変数からユーザー名とパスワードを取得

    # https://mofecoder.com/contests/tuatpc2025spring/tasks/tuatpc2025spring_a から入出力例を取得する
    contest_id, task_slug = "tuatpc2025spring", "tuatpc2025spring_a"
    task = client.get_contest_task(contest_id, task_slug)  # コンテストの問題を取得する

    for i, sample in enumerate(task.samples):
        # 入力例を 1.in, 2.in, ... に、出力例を 1.out, 2.out, ... に保存する

        with open(f"{i + 1}.in", "w") as f:
            f.write(sample.input)

        with open(f"{i + 1}.out", "w") as f:
            f.write(sample.output)
