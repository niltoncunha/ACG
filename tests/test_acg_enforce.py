import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "acg-enforce.py"

spec = importlib.util.spec_from_file_location("acg_enforce", SCRIPT)
acg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acg)


CONFIG = """
project:
  name: fixture
  default_branch: main

task:
  id: fixture-task
  description: "Fixture task"
  scope:
    allowed:
      - src/**
      - tests/**
    forbidden:
      - secrets/**
      - .env
  done_when:
    - command: "python3 -c 'print(123)'"

verify:
  commands:
    - python3 -c "print('ok')"

promotion:
  fail_closed: true
  require_evidence: true
"""


class ACGTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.prev_cwd = os.getcwd()
        os.chdir(self.tmp.name)
        self._git(["init", "-b", "main"])
        self._git(["config", "user.email", "acg@example.local"])
        self._git(["config", "user.name", "ACG Test"])
        Path("acg.yaml").write_text(CONFIG, encoding="utf-8")
        Path("src").mkdir()
        Path("tests").mkdir()
        Path("src/app.py").write_text("print('base')\n", encoding="utf-8")
        self._git(["add", "."])
        self._git(["commit", "-m", "base"])
        self._git(["checkout", "-b", "agent/task"])
        os.environ.pop("GITHUB_HEAD_REF", None)
        os.environ.pop("GITHUB_BASE_REF", None)

    def tearDown(self):
        os.chdir(self.prev_cwd)
        self.tmp.cleanup()

    def _git(self, args):
        cp = subprocess.run(["git", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if cp.returncode != 0:
            raise AssertionError(cp.stdout)
        return cp.stdout.strip()

    def _cfg(self):
        return acg.parse_yaml_subset(Path("acg.yaml"))

    def test_default_branch_is_blocked(self):
        self._git(["checkout", "main"])
        with self.assertRaises(SystemExit):
            acg.check_branch(self._cfg())

    def test_allowed_scope_passes(self):
        Path("src/app.py").write_text("print('changed')\n", encoding="utf-8")
        acg.check_scope(self._cfg())

    def test_outside_scope_is_blocked(self):
        Path("README.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            acg.check_scope(self._cfg())

    def test_forbidden_path_is_blocked(self):
        Path("secrets").mkdir()
        Path("secrets/token.txt").write_text("secret\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            acg.check_scope(self._cfg())

    def test_verify_failure_is_blocked(self):
        bad = CONFIG.replace("python3 -c \"print('ok')\"", "python3 -c \"raise SystemExit(2)\"")
        Path("acg.yaml").write_text(bad, encoding="utf-8")
        with self.assertRaises(SystemExit):
            acg.check_verify(self._cfg())

    def test_all_checks_write_evidence(self):
        Path("src/app.py").write_text("print('changed')\n", encoding="utf-8")
        cfg = self._cfg()
        acg.check_branch(cfg)
        acg.check_scope(cfg)
        acg.check_verify(cfg)
        acg.check_done(cfg)
        acg.check_gate(cfg)
        evidence = Path("acg-evidence.jsonl").read_text(encoding="utf-8")
        self.assertIn('"step": "gate"', evidence)
        self.assertIn('"status": "passed"', evidence)


if __name__ == "__main__":
    unittest.main()
