import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def generate_content(client, messages, verbose):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage is None:
        raise RuntimeError("Failed API request.")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(f"Response: \n{response.choices[0].message.content}")


def main():
    print("Hello from agent-boots!")

    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key was not found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    generate_content(client, messages, args.verbose)


if __name__ == "__main__":
    main()
