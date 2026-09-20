from api_setup import setup_api_key
from model_selections import select_model

from provider.openai_connector import get_reply as openai_reply
from provider.anthropic_connector import get_reply as anthropic_reply
from provider.gemini_connector import get_reply as gemini_reply


def main():

    try:
        provider, model = select_model()
        api_key = setup_api_key(provider)

    except Exception as error:
        print("Setup Error:", error)
        return

    # Select the correct provider function
    connectors = {
        "OpenAI": openai_reply,
        "Anthropic": anthropic_reply,
        "Gemini": gemini_reply
    }

    get_reply = connectors[provider]

    # Temporary conversation context
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    print(f"\n{provider} Chat Started!")
    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            ai_reply = get_reply(api_key, model, messages)

            if not ai_reply:
                raise ValueError("Empty response from model.")

            print("\nAI:", ai_reply, "\n")

            messages.append({
                "role": "assistant",
                "content": ai_reply
            })

        except Exception as error:
            print("API Error:", error)

            # Remove failed user message
            messages.pop()

    print("Chat ended.")


if __name__ == "__main__":
    main()
