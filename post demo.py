# post_demo.py
import urllib.request, json

payload = json.dumps({
    "name": "Intern",
    "task": "API demo"
}).encode("utf-8")

req = urllib.request.Request(
    "<https://httpbin.org/post>",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    result = json.load(resp)

print("Response from httpbin.org:")
print(json.dumps(result, indent=2))