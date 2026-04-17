"""Smoke tests for run_evaluation.py CLI surface."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_help_includes_cases_flag():
    result = subprocess.run(
        [sys.executable, "run_evaluation.py", "--help"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--cases" in result.stdout


def test_case_and_cases_are_mutually_exclusive():
    result = subprocess.run(
        [
            sys.executable,
            "run_evaluation.py",
            "--case",
            "ELEM_01",
            "--cases",
            "ELEM_01,ELEM_02",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Use either --case or --cases" in result.stderr
