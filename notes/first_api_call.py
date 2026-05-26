import os  
import json
import urllib.request


def call_with_sdk():
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Install anthropic SDK by `uv pip install sdk`")

    client = Anthropic(
        # This is the default and can be omitted
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": "In one line, tell me why should we learn AI?"}]
    )
    print(f"SDK response: {response.content[0].text}")
    print(f"Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")

def call_raw_http():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY environment variable first")
        return

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    body = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())

            print("Assistant:", result["content"][0]["text"])
            print(
                f"Tokens used: "
                f"{result['usage']['input_tokens']} in, "
                f"{result['usage']['output_tokens']} out"
            )

    except urllib.error.HTTPError as e:
        print("HTTP Error Code:", e.code)
        print("Error Response:")
        print(e.read().decode())


if __name__=="__main__":

    # print("<-- Using Anthropic SDK -->")
    # call_with_sdk()

    print("<-- Using Raw HTTP -->")
    call_raw_http()