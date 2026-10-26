import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import MAX_ITERATIONS


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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    iterations = 1
    for _ in range(MAX_ITERATIONS):
        # call the model, handle responses, etc.
        message = generate_message(client, messages, args.verbose)
        messages.append(message)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if result_message['content'] is None:
                raise RuntimeError("Failed tool call.")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)

        iterations += 1

    if iterations == MAX_ITERATIONS:
        sys.exit("The agent did not reach a conclusion within the maximum number of iterations.")

    print(f"Response: \n{message.content}")


def generate_message(client, messages, verbose):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Failed API request.")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    return response.choices[0].message


def call_tools(message, messages, verbose):
    '''Each response from the LLM agent should consist of either text or one or more tool calls.'''


if __name__ == "__main__":
    main()
