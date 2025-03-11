import os
import unittest

from mofeapi.client import Client
from mofeapi.enums import Difficulty
from mofeapi.models.problem import ProblemParams

# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=os.environ["MOFE_USERNAME"], password=os.environ["MOFE_PASSWORD"])

    def test_get_contest_tuatpc2025spring(self):
        contest = self.client.get_contest("tuatpc2025spring")
        self.assertEqual(contest.slug, "tuatpc2025spring")
        self.assertEqual(contest.name, "TUATPC 2025 Spring")
        self.assertEqual(contest.penalty_time, 300)
        tasks = contest.tasks
        self.assertEqual(len(tasks), 9)

    def test_get_contest_task_tuatpc2025spring_a(self):
        task = self.client.get_contest_task("tuatpc2025spring", "tuatpc2025spring_a")
        self.assertEqual(task.slug, "tuatpc2025spring_a")
        self.assertEqual(task.name, "628")
        self.assertEqual(task.difficulty, Difficulty.MILK)

    def test_get_problems(self):
        problems = self.client.get_problems()
        self.assertIsInstance(problems, list)

    def test_get_problem_303(self):
        problem = self.client.get_problem(303)
        self.assertEqual(problem.id, 303)
        self.assertEqual(problem.name, "逆転条件")
        self.assertEqual(problem.difficulty, Difficulty.PAKCHI)

    def test_get_problem_306(self):
        problem = self.client.get_problem(306)
        self.assertEqual(problem.id, 306)

    def test_update_problem_306(self):
        problem_params = ProblemParams(
            name="test",
            difficulty=Difficulty.ASSAM,
            statement="test",
            input_format="test",
            output_format="",
            constraints="test",
            execution_time_limit=2000,
            partial_scores="",
            submission_limit_1=5,
            submission_limit_2=60,
        )
        self.client.update_problem(306, problem_params)


if __name__ == "__main__":
    unittest.main()
