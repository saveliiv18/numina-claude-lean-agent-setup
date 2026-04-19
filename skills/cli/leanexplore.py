#!/usr/bin/env python3
"""Search Lean definitions/theorems using lean-explore (semantic search)."""
import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(os.environ.get("CLI_LOG_PATH", Path(__file__).parents[2] / "cli.log")))],
)
logger = logging.getLogger(__name__)


def search(query: str, num_results: int = 5) -> None:
    logger.info("leanexplore.search called: num_results=%d query=%r", num_results, query)
    binary = shutil.which("lean-explore")
    if binary is None:
        logger.error("leanexplore.search failed: `lean-explore` not found on PATH")
        print("Error: `lean-explore` not found on PATH.", file=sys.stderr)
        sys.exit(1)
    try:
        result = subprocess.run(
            [binary, "search", query, "--limit", str(num_results)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as e:
        logger.exception("leanexplore.search timed out: %s", e)
        print("Error: lean-explore timed out.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception("leanexplore.search failed: %s", e)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)

    if result.returncode != 0:
        logger.error("leanexplore.search failed: exit code %d", result.returncode)
        sys.exit(result.returncode)

    logger.info("leanexplore.search succeeded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Lean theorems using lean-explore")
    parser.add_argument("query", help="Search query (natural language, Lean terms, identifiers)")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Max results (default: 5)")
    args = parser.parse_args()
    search(args.query, args.num_results)
