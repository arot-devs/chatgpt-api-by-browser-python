import requests

def get_chat_completion(prompt):
    url = "http://localhost:8766/v1/chat/completions"
    payload = {"text": prompt}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Completion received:")
        print(data["choices"][0]["message"]["content"])
        return data["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

if __name__ == "__main__":
    prompt = "Who is Dtrampt?"
    completion = get_chat_completion(prompt)
