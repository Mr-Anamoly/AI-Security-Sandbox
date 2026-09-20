from getpass import getpass


def setup_api_key(provider):

    api_key = getpass(f"Enter your {provider} API key: ").strip()

    if not api_key:
        raise ValueError("API key cannot be empty.")

    return api_key
