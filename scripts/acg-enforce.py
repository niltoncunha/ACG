#!/usr/bin/env python3
"""ACG-Core minimal enforcement stub.

This repository includes the ACG-Core specification and CI wiring.
For the full local enforcement implementation, use the packaged release ZIP or replace this file with your preferred CI runner.

Minimum contract:
- run outside the default branch;
- check changed files against acg.yaml scope;
- run verification outside the agent;
- fail closed when evidence is missing or failed.
"""

import sys
from pathlib import Path


def main() -> int:
    config = Path("acg.yaml")
    if not config.exists():
        print("ACG BLOCKED: acg.yaml not found")
        return 1
    print("ACG-Core minimal stub: config found.")
    print("Replace scripts/acg-enforce.py with the full enforcement runner before using this in production.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
