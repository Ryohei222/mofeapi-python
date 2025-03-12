import json
from dataclasses import asdict
from typing import List, Tuple

import requests
from dacite import Config, from_dict

from mofeapi.enums import AggregateType, ContestKind, Difficulty, PublicStatus, StandingsMode
from mofeapi.models.contest import Contest, ContestDetail
from mofeapi.models.post import Post
from mofeapi.models.problem import Problem, ProblemDetail, ProblemParams
from mofeapi.models.task import TaskDetail
from mofeapi.models.testcase import Testcase, TestcaseDetail, TestcaseParams, TestcaseSet, TestcaseSetBase

API_URL = "https://api.mofecoder.com/api"
LOGIN_URL = "https://api.mofecoder.com/api/auth/sign_in"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Difficulty):
            return obj.value
        if isinstance(obj, AggregateType):
            return obj.value
        return super().default(obj)


class Client:
    def __init__(self):
        self.logined = False
        self.headers = None

    def login(self, username: str, password: str) -> int:
        data = {"name": username, "password": password}
        try:
            response = requests.post(LOGIN_URL, data=data)
            response.raise_for_status()
            self.logined = True
            self.headers = {
                "client": response.headers["client"],
                "Authorization": response.headers["Authorization"],
                "uid": response.headers["uid"],
                "access-token": response.headers["access-token"],
            }
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return response.status_code if response else 500
        return response.status_code

    def _request(self, method: str, path: str, headers={}, expected_status_code: int = 200, **kwargs) -> dict:
        if not self.logined:
            print("Not logged in")
            raise Exception("Not logged in")
        try:
            response = requests.request(method, API_URL + path, headers=self.headers | headers, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        if response.status_code != expected_status_code:
            print(f"Expected status code {expected_status_code}, but got {response.status_code}")
            print(response.text)
            raise Exception("Request failed")
        if response.status_code == 201 or response.status_code == 204:
            return {}
        return response.json()

    # https://github.com/mofecoder/mofe-front/blob/7e32b10a93c7e515f6e94fe5f46bb8d0cc86ce5f/app/utils/apis/index.ts

    def top(self) -> Tuple[List[ContestDetail], List[Problem], List[Post]]:
        """トップページの情報(直近のコンテスト・作成中の問題・記事)を取得する

        Returns:
            Tuple[List[ContestDetail], List[Problem], List[Post]]: 直近のコンテスト, 作成中の問題, 記事
        """
        response = self._request("GET", "/top")
        contests = [
            from_dict(data_class=Contest, data=contest, config=Config(cast=[Difficulty, ContestKind, StandingsMode]))
            for contest in response["contests"]
        ]
        problems = [
            from_dict(data_class=Problem, data=problem, config=Config(cast=[Difficulty]))
            for problem in response["creating"]
        ]
        posts = [
            from_dict(data_class=Post, data=post, config=Config(cast=[PublicStatus])) for post in response["posts"]
        ]
        return contests, problems, posts

    # TODO: 次のメソッドを実装する
    # changeTestcaseState,
    # updateChecker,
    # downloadChecker
    # (getUnsetProblems),
    # (addTester),
    # (removeTester),
    # (createProblem),

    # /problems https://github.com/mofecoder/mofe-front/blob/master/app/utils/apis/ManageProblems.ts
    def get_problem(self, problem_id: int) -> ProblemDetail:
        response = self._request("GET", f"/problems/{problem_id}")
        return from_dict(data_class=ProblemDetail, data=response, config=Config(cast=[Difficulty, ContestKind]))

    def get_problems(self) -> list[Problem]:
        response = self._request("GET", "/problems")
        return [from_dict(data_class=Problem, data=problem, config=Config(cast=[Difficulty])) for problem in response]

    def update_problem(self, problem_id: int, problem: ProblemParams) -> ProblemDetail:
        data = json.loads(json.dumps(asdict(problem), cls=CustomJSONEncoder))
        response = self._request("PUT", f"/problems/{problem_id}", json={"problem": data})
        return from_dict(data_class=ProblemDetail, data=response, config=Config(cast=[Difficulty, ContestKind]))

    # /problems/{problem_id}/testcases

    def get_testcases(self, problem_id: int) -> Tuple[List[TestcaseSet], List[Testcase]]:
        response = self._request("GET", f"/problems/{problem_id}/testcases")
        testcase_sets = [
            from_dict(data_class=TestcaseSet, data=testcase_set, config=Config(cast=[AggregateType]))
            for testcase_set in response["testcase_sets"]
        ]
        testcases = [from_dict(data_class=Testcase, data=testcase) for testcase in response["testcases"]]
        return testcase_sets, testcases

    def get_testcase(self, problem_id: int, testcase_id: int) -> TestcaseDetail:
        response = self._request("GET", f"/problems/{problem_id}/testcases/{testcase_id}")
        return from_dict(data_class=TestcaseDetail, data=response)

    def update_testcase(self, problem_id: int, testcase_id: int, testcase: TestcaseDetail) -> None:
        self._request(
            "PUT", f"/problems/{problem_id}/testcases/{testcase_id}", json=asdict(testcase), expected_status_code=204
        )

    def create_testcase(self, problem_id: int, testcase: TestcaseParams) -> None:
        self._request("POST", f"/problems/{problem_id}/testcases", json=asdict(testcase), expected_status_code=201)

    def delete_multiple_testcases(self, problem_id: int, testcase_ids: List[int]) -> None:
        self._request(
            "DELETE",
            f"/problems/{problem_id}/testcases/delete_multiple",
            json={"testcases": testcase_ids},
            expected_status_code=204,
        )

    def delete_testcase(self, problem_id: int, testcase_id: int) -> None:
        self.delete_multiple_testcases(problem_id, [testcase_id])

    def get_testcase_set(self, problem_id: int, testcase_set_id: int) -> TestcaseSet:
        response = self._request("GET", f"/problems/{problem_id}/testcase_sets/{testcase_set_id}")
        return from_dict(data_class=TestcaseSet, data=response, config=Config(cast=[AggregateType]))

    def update_testcase_set(self, problem_id: int, testcase_set_id: int, testcase_set: TestcaseSetBase) -> None:
        data = json.loads(json.dumps(asdict(testcase_set), cls=CustomJSONEncoder))
        self._request(
            "PUT",
            f"/problems/{problem_id}/testcase_sets/{testcase_set_id}",
            json=data,
            expected_status_code=204,
        )

    def create_testcase_set(self, problem_id: int, testcase_set: TestcaseSetBase) -> None:
        data = json.loads(json.dumps(asdict(testcase_set), cls=CustomJSONEncoder))
        self._request("POST", f"/problems/{problem_id}/testcase_sets", json=data, expected_status_code=201)

    def delete_testcase_set(self, problem_id: int, testcase_set_id: int) -> None:
        self._request(
            "DELETE",
            f"/problems/{problem_id}/testcase_sets/{testcase_set_id}",
            expected_status_code=204,
        )

    def add_to_testcase_set_multiple(self, problem_id: int, testcase_set_id: int, testcase_ids: List[int]) -> None:
        self._request(
            "PATCH",
            f"/problems/{problem_id}/testcases/change_state_multiple",
            json={"testcase_ids": testcase_ids, "testcase_set_id": testcase_set_id},
            expected_status_code=204,
        )

    def upload_testcases(self, problem_id: int, file: bytes) -> None:
        self._request(
            "POST",
            f"/problems/{problem_id}/testcases/upload",
            files={"file": file},
            expected_status_code=200,
        )

    # /contests
    def get_contest(self, contest_id: str) -> ContestDetail:
        response = self._request("GET", f"/contests/{contest_id}")
        return from_dict(
            data_class=ContestDetail, data=response, config=Config(cast=[Difficulty, ContestKind, StandingsMode])
        )

    def get_contest_task(self, contest_id: str, task_id: str) -> TaskDetail:
        response = self._request("GET", f"/contests/{contest_id}/tasks/{task_id}")
        return from_dict(data_class=TaskDetail, data=response, config=Config(cast=[Difficulty]))
