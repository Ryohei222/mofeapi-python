import requests
import json
from mofeapi.models.contest import ContestDetail
from mofeapi.models.task import Task
from mofeapi.models.problem import ProblemDetail
from typing import List, Tuple, Optional
import re

API_URL = 'https://api.mofecoder.com/api'
LOGIN_URL = 'https://api.mofecoder.com/api/auth/sign_in'

class Client:
    def __init__(self):
        self.logined = False
        self.headers = None

    def login(self, username: str, password: str) -> int:
        data = {
            'name': username,
            'password': password
        }
        try:
            response = requests.post(LOGIN_URL, data=data)
            response.raise_for_status()
            self.logined = True
            self.headers = {
                'client': response.headers['client'],
                'Authorization': response.headers['Authorization'],
                'uid': response.headers['uid'],
                'access-token': response.headers['access-token']
            }
        except requests.exceptions.RequestException as e:
            print(f'Login failed: {e}')
            return response.status_code if response else 500
        return response.status_code

    def _request(self, method: str, url: str, headers={}, **kwargs):
        if not self.logined:
            print('Not logged in')
            return None
        try:
            # print('-'*50)
            # print(f'[+] {method} {API_URL + url} headers={self.headers | headers}, kwargs={kwargs}')
            response = requests.request(method, API_URL + url, headers=self.headers | headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
            return None

    def get_contest(self, contest_id: str) -> ContestDetail:
        response = self._request('GET', f'/contests/{contest_id}')
        return ContestDetail.from_dict(response.json())

    def get_contest_task(self, contest_id: str, task_id: str) -> Task:
        response = self._request('GET', f'/contests/{contest_id}/tasks/{task_id}')
        return Task.from_dict(response.json())

    def get_problem(self, problem_id: int) -> Task:
        response = self._request('GET', f'/problems/{problem_id}')
        return ProblemDetail.from_dict(response.json())