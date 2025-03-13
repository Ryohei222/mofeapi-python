import logging
import os
import unittest

from mofeapi.client import Client
from mofeapi.enums import AggregateType, Difficulty
from mofeapi.models.contest import Contest
from mofeapi.models.post import Post
from mofeapi.models.problem import Problem, ProblemParams
from mofeapi.models.testcase import TestcaseDetail, TestcaseParams, TestcaseSet, TestcaseSetBase


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
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

    def test_get_problem_296(self):
        problem = self.client.get_problem(296)
        self.assertEqual(problem.id, 296)
        self.assertEqual(problem.name, "ngng 文字列")
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

    def test_get_testcase_problem_303_31554(self):
        testcase = self.client.get_testcase(303, 31554)
        self.assertIsInstance(testcase, TestcaseDetail)
        self.assertEqual(testcase.id, 31554)
        self.assertEqual(testcase.name, "00_sample_01")

    def test_update_testcase_problem_306_34707(self):
        testcase = TestcaseDetail(
            id=34707,
            name="00_sample_01",
            input="1\n",
            output="1\n",
            explanation="",
        )
        self.client.update_testcase(306, testcase.id, testcase)

    def test_get_testcase_set_problem_303_833(self):
        testcase_set = self.client.get_testcase_set(303, 833)
        self.assertIsInstance(testcase_set, TestcaseSet)
        self.assertEqual(testcase_set.id, 833)
        self.assertEqual(testcase_set.name, "sample")
        self.assertEqual(testcase_set.points, 0)
        self.assertEqual(testcase_set.aggregate_type, AggregateType.ALL)
        self.assertEqual(testcase_set.is_sample, True)

    def test_update_testcase_set_problem_306_916(self):
        testcase_set = TestcaseSetBase(
            name="mofeapi-test-sample",
            points=100,
            aggregate_type=AggregateType.SUM,
        )
        self.client.update_testcase_set(306, 916, testcase_set)
        updated_testcase_set = self.client.get_testcase_set(306, 916)
        self.assertEqual(updated_testcase_set.name, testcase_set.name)
        self.assertEqual(updated_testcase_set.points, testcase_set.points)
        self.assertEqual(updated_testcase_set.aggregate_type, testcase_set.aggregate_type)

    def test_add_to_testcase_set_multiple(self):
        problem_id = 306
        testcase_set_id = 916
        testcase_ids = [34707, 34708, 34709]

        self.client.add_to_testcase_set_multiple(problem_id, testcase_set_id, testcase_ids)

        testcase_sets, testcases = self.client.get_testcases(problem_id)

        for testcase_set_index, testcase_set in enumerate(testcase_sets):
            if testcase_set.name != "mofeapi-test-sample":
                continue
            for testcase in testcases:
                self.assertTrue(testcase.testcase_sets[testcase_set_index])

    def test_create_testcase(self):
        problem_id = 306
        testcase_name = "99_mofeapi_01"
        testcase_params = TestcaseParams(
            name=testcase_name,
            input="1\n",
            output="1\n",
            explanation="Sample explanation",
        )

        _, testcases = self.client.get_testcases(problem_id)

        for testcase in testcases:
            if testcase.name == testcase_name:
                self.client.delete_multiple_testcases(problem_id, [testcase.id])

        self.client.create_testcase(problem_id, testcase_params)

        _, updated_testcases = self.client.get_testcases(problem_id)
        created_testcase_id = next((tc for tc in updated_testcases if tc.name == "99_mofeapi_01"), None)

        created_testcase_detail = self.client.get_testcase(problem_id, created_testcase_id.id)

        self.assertIsNotNone(created_testcase_detail)
        self.assertEqual(created_testcase_detail.input, testcase_params.input)
        self.assertEqual(created_testcase_detail.output, testcase_params.output)
        self.assertEqual(created_testcase_detail.explanation, testcase_params.explanation)

    def test_create_testcase_set(self):
        problem_id = 306
        testcase_set_params = TestcaseSetBase(
            name="mofeapi-new-testcase-set",
            points=50,
            aggregate_type=AggregateType.ALL,
        )

        # Ensure the testcase set does not already exist
        testcase_sets, _ = self.client.get_testcases(problem_id)
        for testcase_set in testcase_sets:
            if testcase_set.name == testcase_set_params.name:
                self.client.delete_testcase_set(problem_id, testcase_set.id)

        # Create the new testcase set
        self.client.create_testcase_set(problem_id, testcase_set_params)

        # Verify the testcase set was created
        new_testcase_sets, _ = self.client.get_testcases(problem_id)
        created_testcase_set = next((ts for ts in new_testcase_sets if ts.name == testcase_set_params.name), None)

        self.assertIsNotNone(created_testcase_set)
        self.assertEqual(created_testcase_set.name, testcase_set_params.name)
        self.assertEqual(created_testcase_set.points, testcase_set_params.points)
        self.assertEqual(created_testcase_set.aggregate_type, AggregateType.ALL)

    def test_top(self):
        contests, problems, posts = self.client.top()
        self.assertIsInstance(contests, list)
        self.assertTrue(all(isinstance(contest, Contest) for contest in contests))

        self.assertIsInstance(problems, list)
        self.assertTrue(all(isinstance(problem, Problem) for problem in problems))

        self.assertIsInstance(posts, list)
        self.assertTrue(all(isinstance(post, Post) for post in posts))


if __name__ == "__main__":
    unittest.main()
