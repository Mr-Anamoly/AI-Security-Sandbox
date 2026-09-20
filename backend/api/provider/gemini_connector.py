from google import genai
from google.genai import types

def get_reply(api_key, model, messages):

    client = genai.Client(api_key=api_key)

    system = ""
    history = []

    for msg in messages:

        if msg["role"] == "system":
            system = msg["content"]

        else:
            role = "model" if msg["role"] == "assistant" else "user"

            history.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

    response = client.models.generate_content(
        model=model,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system
        )
    )

    return response.text