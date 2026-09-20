PROVIDERS = {
    "1": "OpenAI",
    "2": "Anthropic",
    "3": "Gemini"
}

MODELS = {
    "OpenAI": ["gpt-4.1", "gpt-4.1-mini"],
    "Anthropic": ["claude-sonnet-4-5"],
    "Gemini": ["gemini-2.5-flash"]
}


def select_model():

    print("\nSelect Provider:")

    for key, name in PROVIDERS.items():
        print(f"{key}. {name}")

    choice = input("Choice: ").strip()

    if choice not in PROVIDERS:
        raise ValueError("Invalid provider.")

    provider = PROVIDERS[choice]
    models = MODELS[provider]

    print(f"\n{provider} Models:")

    for i, name in enumerate(models, 1):
        print(f"{i}. {name}")

    print(f"{len(models) + 1}. Custom model")

    choice = input("Select model: ").strip()

    if choice == str(len(models) + 1):
        model = input("Enter model ID: ").strip()

    elif choice.isdigit() and 1 <= int(choice) <= len(models):
        model = models[int(choice) - 1]

    else:
        raise ValueError("Invalid model selection.")

    if not model:
        raise ValueError("Model ID cannot be empty.")

    return provider, model