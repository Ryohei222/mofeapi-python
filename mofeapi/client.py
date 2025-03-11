import json
from dataclasses import asdict

import requests
from dacite import Config, from_dict

from mofeapi.enums import ContestKind, Difficulty, StandingsMode
from mofeapi.models.contest import ContestDetail
from mofeapi.models.problem import Problem, ProblemDetail, ProblemParams
from mofeapi.models.task import TaskDetail

API_URL = "https://api.mofecoder.com/api"
LOGIN_URL = "https://api.mofecoder.com/api/auth/sign_in"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Difficulty):
            return obj.value  # or obj.name
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

    def _request(self, method: str, path: str, headers={}, **kwargs) -> dict:
        if not self.logined:
            print("Not logged in")
            raise Exception("Not logged in")
        try:
            response = requests.request(method, API_URL + path, headers=self.headers | headers, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return response.json()

    def get_contest(self, contest_id: str) -> ContestDetail:
        response = self._request("GET", f"/contests/{contest_id}")
        return from_dict(
            data_class=ContestDetail, data=response, config=Config(cast=[Difficulty, ContestKind, StandingsMode])
        )

    # /problems https://github.com/mofecoder/mofe-front/blob/master/app/utils/apis/ManageProblems.ts
    def get_problem(self, problem_id: int) -> ProblemDetail:
        response = self._request("GET", f"/problems/{problem_id}")
        return from_dict(data_class=ProblemDetail, data=response, config=Config(cast=[Difficulty]))

    def get_problems(self) -> list[Problem]:
        response = self._request("GET", "/problems")
        return [from_dict(data_class=Problem, data=problem, config=Config(cast=[Difficulty])) for problem in response]

    def update_problem(self, problem_id: int, problem: ProblemParams) -> ProblemDetail:
        data = json.loads(json.dumps(asdict(problem), cls=CustomJSONEncoder))
        response = self._request("PUT", f"/problems/{problem_id}", json={"problem": data})
        return from_dict(data_class=ProblemDetail, data=response, config=Config(cast=[Difficulty]))

    def get_contest_task(self, contest_id: str, task_id: str) -> TaskDetail:
        response = self._request("GET", f"/contests/{contest_id}/tasks/{task_id}")
        return from_dict(data_class=TaskDetail, data=response, config=Config(cast=[Difficulty]))

    # def create_problem(self, problem: ProblemParams) -> ProblemDetail:
    #     response = self._request('POST', '/problems', json=problem.__dict__)
    #     return ProblemDetail.from_dict(response.json())

    # def get_testcase(self, problem_id: int, testcase_id: int) -> Testcase:
    #     return self._get(f'/problems/{problem_id}/testcases/{testcase_id}', Testcase)
