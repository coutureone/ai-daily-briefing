#!/usr/bin/env python3
"""Send the generated daily briefing to a DingTalk group robot."""

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import urllib.request


def build_signed_webhook(webhook: str, secret: str | None) -> str:
    """Append DingTalk robot signature parameters when a secret is configured."""
    if not secret:
        return webhook

    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(digest))
    separator = "&" if "?" in webhook else "?"
    return f"{webhook}{separator}timestamp={timestamp}&sign={sign}"


def read_briefing(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read().strip()


def send_markdown(webhook: str, secret: str | None, title: str, text: str) -> None:
    url = build_signed_webhook(webhook, secret)
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text,
        },
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")

    result = json.loads(body)
    if result.get("errcode") != 0:
        raise RuntimeError(f"DingTalk robot returned an error: {body}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a briefing file to DingTalk.")
    parser.add_argument("briefing_file", help="Path to the generated briefing text file.")
    parser.add_argument("--title", default="每日 AI 早报", help="DingTalk message title.")
    args = parser.parse_args()

    webhook = os.environ.get("DINGTALK_WEBHOOK")
    secret = os.environ.get("DINGTALK_SECRET")

    if not webhook:
        print("Missing required environment variable: DINGTALK_WEBHOOK", file=sys.stderr)
        return 1

    text = read_briefing(args.briefing_file)
    if not text:
        print(f"Briefing file is empty: {args.briefing_file}", file=sys.stderr)
        return 1

    send_markdown(webhook, secret, args.title, text)
    print("DingTalk briefing sent successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
