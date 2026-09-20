from anthropic import Anthropic


def get_reply(api_key, model, messages):

    client = Anthropic(api_key=api_key)

    system = ""
    history = []

    for msg in messages:

        if msg["role"] == "system":
            system = msg["content"]

        else:
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=history
    )

    return "".join(
        block.text
        for block in response.content
        if block.type == "text"
    )