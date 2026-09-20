from openai import OpenAI


def get_reply(api_key, model, messages):

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=messages
    )

    return response.output_text