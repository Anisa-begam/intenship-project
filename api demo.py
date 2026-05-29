# api_demo.py
import urllib.request, json

def get_joke():
    with urllib.request.urlopen(
        "<https://official-joke-api.appspot.com/random_joke>"
    ) as resp:
        data = json.load(resp)
    return f"{data['setup']} – {data['punchline']}"

if __name__ == "__main__":
    print("Here's a joke for you:")
    print(get_joke())