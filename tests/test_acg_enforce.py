from __future__ import annotations

import importlib.util
import subprocess
import textwrap
import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "acg-enforce.py"
BOOTSTRAP = REPO_ROOT / "scripts" / "acg-bootstrap.py"
SPEC = importlib.util.spec_from_file_location("acg_enforce", SCRIPT)
assert SPEC and SPEC.loader
ACG_ENFORCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ACG_ENFORCE)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


class ACGEnforceTests(unittest.TestCase):
    def write_config(self, root: Path, extra: str = "") -> Path:
        config = textwrap.dedent(
            f"""
            project:
              name: sample
              default_branch: main

            task:
              id: sample-task
              description: "sample"
              scope:
                allowed:
                  - src/**
                  - tests/**
                  - scripts/**
                  - README.md
                  - acg.yaml
                forbidden:
                  - secrets/**
              done_when:
                - file_exists: "README.md"
            verify:
              commands:
                - python3 -c "print('verify ok')"
            promotion:
              fail_closed: true
              require_evidence: true
            """
        ).strip()
        path = root / "acg.yaml"
        path.write_text(config + ("\n" + extra.strip() if extra.strip() else "") + "\n", encoding="utf-8")
        return path

    def init_git_repo(self, root: Path, branch: str = "feature/test") -> None:
        run(["git", "init", "-b", "main"], cwd=root)
        run(["git", "config", "user.email", "test@example.com"], cwd=root)
        run(["git", "config", "user.name", "Test User"], cwd=root)
        (root / "README.md").write_text("base\n", encoding="utf-8")
        run(["git", "add", "README.md"], cwd=root)
        run(["git", "commit", "-m", "init"], cwd=root)
        run(["git", "checkout", "-b", branch], cwd=root)

    def test_branch_fails_on_default_branch(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root, branch="feature/test")
            run(["git", "checkout", "main"], cwd=root)
            config = self.write_config(root)

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "branch"], cwd=root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("current branch is default branch", result.stdout)

    def test_scope_fails_for_out_of_scope_file(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            (root / "notes.txt").write_text("bad\n", encoding="utf-8")

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "scope"], cwd=root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside allowed scope: notes.txt", result.stdout)

    def test_scope_fails_for_forbidden_file(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            (root / "secrets").mkdir()
            (root / "secrets" / "prod.env").write_text("token\n", encoding="utf-8")

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "scope"], cwd=root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("forbidden touched: secrets/prod.env", result.stdout)

    def test_verify_fails_when_command_fails(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = root / "acg.yaml"
            config.write_text(
                textwrap.dedent(
                    """
                    project:
                      name: sample
                      default_branch: main
                    task:
                      id: sample-task
                      description: "sample"
                      scope:
                        allowed:
                          - README.md
                        forbidden:
                          - secrets/**
                    verify:
                      commands:
                        - python3 -c "raise SystemExit(1)"
                    promotion:
                      fail_closed: true
                      require_evidence: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "verify"], cwd=root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ACG BLOCKED: verification failed", result.stdout)

    def test_all_mode_writes_evidence_and_logs(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            (root / "src").mkdir()
            (root / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "all"], cwd=root)

            self.assertEqual(result.returncode, 0, result.stdout)
            evidence = (root / "acg-evidence.jsonl").read_text(encoding="utf-8")
            self.assertIn('"step": "gate"', evidence)
            self.assertTrue((root / "acg-logs").exists())

    def test_scope_uses_merge_base_when_main_moves(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            (root / "src").mkdir()
            (root / "src" / "feature.py").write_text("print('feature')\n", encoding="utf-8")
            run(["git", "add", "src/feature.py"], cwd=root)
            run(["git", "commit", "-m", "feature work"], cwd=root)

            run(["git", "checkout", "main"], cwd=root)
            (root / "README.md").write_text("base moved\n", encoding="utf-8")
            run(["git", "add", "README.md"], cwd=root)
            run(["git", "commit", "-m", "main moved"], cwd=root)
            run(["git", "checkout", "feature/test"], cwd=root)

            result = run(["python3", str(SCRIPT), "--config", str(config), "--mode", "scope"], cwd=root)

            self.assertEqual(result.returncode, 0, result.stdout)
            evidence = (root / "acg-evidence.jsonl").read_text(encoding="utf-8")
            self.assertIn('"changed_files": ["src/feature.py"]', evidence)

    def test_scope_blocks_parent_traversal_path(self) -> None:
        cfg = {
            "project": {"default_branch": "main"},
            "task": {"id": "sample-task", "scope": {"allowed": ["src/**"], "forbidden": ["secrets/**"]}},
        }

        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            original = ACG_ENFORCE.changed_files
            try:
                ACG_ENFORCE.changed_files = lambda *_args, **_kwargs: ["src/../notes.txt"]
                with self.assertRaises(SystemExit):
                    ACG_ENFORCE.check_scope(cfg, root, config)
            finally:
                ACG_ENFORCE.changed_files = original

    def test_scope_blocks_absolute_path(self) -> None:
        cfg = {
            "project": {"default_branch": "main"},
            "task": {"id": "sample-task", "scope": {"allowed": ["**"], "forbidden": ["secrets/**"]}},
        }

        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.init_git_repo(root)
            config = self.write_config(root)
            original = ACG_ENFORCE.changed_files
            try:
                ACG_ENFORCE.changed_files = lambda *_args, **_kwargs: ["/tmp/secrets/prod.env"]
                with self.assertRaises(SystemExit):
                    ACG_ENFORCE.check_scope(cfg, root, config)
            finally:
                ACG_ENFORCE.changed_files = original

    def test_bootstrap_generates_config(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text("hello\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_smoke.py").write_text("print('ok')\n", encoding="utf-8")
            output = root / "acg.generated.yaml"

            result = run(
                ["python3", str(BOOTSTRAP), "--repo", str(root), "--output", str(output)],
                cwd=root,
            )

            self.assertEqual(result.returncode, 0, result.stdout)
            content = output.read_text(encoding="utf-8")
            self.assertIn("name:", content)
            self.assertIn("src/**", content)
            self.assertIn("tests/**", content)
            self.assertIn("python3 -m unittest discover -s tests -p 'test_*.py'", content)

    def test_schema_files_are_valid_json(self) -> None:
        schema_dir = REPO_ROOT / "schemas"
        for schema_name in ("acg-evidence.schema.json", "scout-report.schema.json"):
            payload = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
            self.assertIn("title", payload)
            self.assertIn("type", payload)


if __name__ == "__main__":
    unittest.main()
