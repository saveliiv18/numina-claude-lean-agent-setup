#!/usr/bin/env python3
"""Get diagnostic messages (errors, warnings, infos) from a Lean 4 verification server."""
import argparse
import json
import logging
import os
import sys
import uuid
from pathlib import Path

import requests
import tenacity

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(__file__).parents[2] / "cli.log")],
)
logger = logging.getLogger(__name__)


def query_server(url: str, code: str, timeout: int = 300, n_retries: int = 10) -> dict:
    """Send code to the Lean 4 server and return the response."""
    json_data = {
        "method": "one_pass_verify_batch",
        "codes": [{"code": code, "custom_id": str(uuid.uuid4())}],
        "timeout": timeout,
    }

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(n_retries),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=lambda state: logger.exception(state.outcome.exception()),
    )
    def _post():
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp = requests.post(
            f"{url}/one_pass_verify_batch",
            headers=headers,
            json=json_data,
        )
        return resp.json()

    return _post()


def format_diagnostics(messages: list[dict]) -> list[str]:
    """Format diagnostic messages similar to lean-lsp-mcp format_diagnostics."""
    msgs = []
    for msg in messages:
        severity = msg.get("severity", "unknown")
        data = msg.get("data", "")
        pos_start = msg.get("pos", {})
        pos_end = msg.get("endPos", {})
        if pos_start and pos_end:
            r_text = (
                f"l{pos_start.get('line', '?')}c{pos_start.get('column', '?')}"
                f"-l{pos_end.get('line', '?')}c{pos_end.get('column', '?')}"
            )
        else:
            r_text = "No range"
        msgs.append(f"{r_text}, severity: {severity}\n{data}")
    return msgs


def diagnostic(code: str, url: str, timeout: int = 300) -> None:
    logger.info("diagnostic called: url=%s code_len=%d timeout=%d", url, len(code), timeout)
    try:
        response = query_server(url, code, timeout=timeout)

        # Extract the single result
        if "results" in response:
            assert len(response["results"]) == 1
            response = response["results"][0]

        result = response.get("response", response)

        # Check for top-level errors
        if "error" in result:
            logger.warning("diagnostic: server returned error: %s", result["error"])
            print(json.dumps({"error": result["error"]}, indent=2, ensure_ascii=False))
            return

        if "stderr" in result:
            logger.warning("diagnostic: server returned stderr: %s", result["stderr"])
            print(json.dumps({"stderr": result["stderr"]}, indent=2, ensure_ascii=False))
            return

        # Format diagnostic messages
        messages = result.get("messages", [])
        formatted = format_diagnostics(messages)

        output = {
            "has_error": any(
                m.get("severity") == "error" for m in messages
            ),
            "diagnostics": formatted,
            "raw_messages": messages,
        }
        logger.info("diagnostic succeeded: %d messages, has_error=%s", len(messages), output["has_error"])
        print(json.dumps(output, indent=2, ensure_ascii=False))

    except Exception as e:
        logger.exception("diagnostic failed: %s", e)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get diagnostic messages from a Lean 4 server")
    parser.add_argument("code", help="Lean 4 code string, or path to a .lean file")
    parser.add_argument("-u", "--url", default=os.environ.get("LEAN4_SERVER_URL", "http://localhost:6666"), help="Server URL (default: $LEAN4_SERVER_URL or http://localhost:6666)")
    parser.add_argument("-t", "--timeout", type=int, default=300, help="Timeout in seconds (default: 300)")
    args = parser.parse_args()

    # If the code argument is a file path, read its contents
    code_path = Path(args.code)
    if code_path.exists() and code_path.suffix == ".lean":
        code = code_path.read_text()
    else:
        code = args.code

    diagnostic(code, args.url, args.timeout)
