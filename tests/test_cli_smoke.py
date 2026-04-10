from __future__ import annotations

import contextlib
import io
import unittest

from dormant_behavior_audit import cli


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str]:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = cli.main(list(args))
        return code, stream.getvalue()

    def test_help(self) -> None:
        code, output = self.run_cli("help")
        self.assertEqual(code, 0)
        self.assertIn("Dormant Behavior Audit CLI", output)

    def test_list_tasks(self) -> None:
        code, output = self.run_cli("list-tasks")
        self.assertEqual(code, 0)
        self.assertIn("meridian_trace_multiturn_candidate_v0", output)

    def test_show_task(self) -> None:
        code, output = self.run_cli("show-task", "qwen2_7b_multiturn_clean_control_v0")
        self.assertEqual(code, 0)
        self.assertIn("qwen2_7b_multiturn_clean_control_v0", output)

    def test_list_submissions(self) -> None:
        code, output = self.run_cli("list-submissions")
        self.assertEqual(code, 0)
        self.assertIn("qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0", output)

    def test_scoreboard(self) -> None:
        code, output = self.run_cli("scoreboard")
        self.assertEqual(code, 0)
        self.assertIn("Submission Scoreboard", output)


if __name__ == "__main__":
    unittest.main()
