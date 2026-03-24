#!/usr/bin/env python3
"""Search premises by proof state using Lean Hammer premise search."""
import argparse
import json
import os
import sys
import urllib.request


def search(goal: str, num_results: int = 32) -> None:
    try:
        base_url = os.getenv("LEAN_HAMMER_URL", "http://leanpremise.net")
        data = json.dumps({
            "state": goal,
            "new_premises": [],
            "k": num_results,
        }).encode()

        req = urllib.request.Request(
            base_url + "/retrieve",
            headers={
                "User-Agent": "numina-lean-agent/0.1",
                "Content-Type": "application/json",
            },
            method="POST",
            data=data,
        )

        with urllib.request.urlopen(req, timeout=20) as response:
            results = json.loads(response.read())

        names = [result["name"] for result in results]
        print(json.dumps(names, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search premises by proof state (Lean Hammer)")
    parser.add_argument("goal", help="Proof state / goal text")
    parser.add_argument("-n", "--num-results", type=int, default=32, help="Max results (default: 32)")
    args = parser.parse_args()
    search(args.goal, args.num_results)
