#!/usr/bin/env python3
"""Search Lean definitions/theorems using lean-explore (semantic search), with Leandex fallback."""
import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(os.environ.get("CLI_LOG_PATH", Path(__file__).parents[2] / "cli.log")))],
)
logger = logging.getLogger(__name__)


def _search_via_leandex(query: str, num_results: int) -> None:
    logger.info("leanexplore: falling back to leandex for query=%r", query)
    url = "https://leandex.projectnumina.ai/api/v1/search"
    params = {
        "q": query,
        "limit": num_results,
        "generate_query": False,
        "analyze_result": False,
    }
    headers = {
        "accept": "text/event-stream",
        "user-agent": "numina-lean-agent/0.1",
    }

    data = None
    with requests.get(url, headers=headers, params=params, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data:"):
                data = line.removeprefix("data:").strip()

    if data is None:
        raise RuntimeError("No data received from Leandex")

    parsed = json.loads(data)
    results = parsed["data"]["search_results"]
    for r in results:
        r["primary_declaration"] = r["primary_declaration"]["lean_name"]

    logger.info("leandex fallback succeeded: %d results", len(results))
    print(json.dumps(results, indent=2, ensure_ascii=False))


def search(query: str, num_results: int = 5) -> None:
    logger.info("leanexplore.search called: num_results=%d query=%r", num_results, query)
    binary = shutil.which("lean-explore")

    if binary is not None and os.environ.get("LEANEXPLORE_API_KEY"):
        try:
            result = subprocess.run(
                [binary, "search", query, "--limit", str(num_results)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="", file=sys.stderr)
                logger.info("leanexplore.search succeeded")
                return
            logger.warning(
                "lean-explore exited with code %d, falling back to leandex", result.returncode
            )
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
        except subprocess.TimeoutExpired:
            logger.warning("lean-explore timed out, falling back to leandex")
        except Exception as e:
            logger.warning("lean-explore error (%s), falling back to leandex", e)
    else:
        if binary is None:
            logger.warning("`lean-explore` not found on PATH, falling back to leandex")
        else:
            logger.warning("LEANEXPLORE_API_KEY not set, falling back to leandex")

    try:
        _search_via_leandex(query, num_results)
    except Exception as e:
        logger.exception("leandex fallback also failed: %s", e)
        print(f"Error: both lean-explore and leandex failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Lean theorems using lean-explore (with Leandex fallback)")
    parser.add_argument("query", help="Search query (natural language, Lean terms, identifiers)")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Max results (default: 5)")
    args = parser.parse_args()
    search(args.query, args.num_results)
