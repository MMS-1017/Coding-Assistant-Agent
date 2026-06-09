import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions import call_function, schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in environment or .env file")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Usage: python main.py \"<prompt>\" [--verbose]")
        sys.exit(1)

    verbose = len(sys.argv) == 3 and sys.argv[2] == "--verbose"
    prompt = sys.argv[1]

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan.
        You can perform the following operations:

        - List files and directories
        - Read file contents
        - Write to a file
        - Run a Python file with optional arguments

        All paths you provide should be relative to the working directory.
        You do not need to specify the working directory in your function calls as it is
        automatically injected for security reasons.
    """

    messages: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0,
    )

    max_iters = 20
    for i in range(max_iters):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        if response is None or response.usage_metadata is None:
            print("Error: Received malformed response from API")
            return

        if verbose:
            print(f"\n[Iteration {i + 1}]")
            print(f"Prompt tokens : {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                function_response_content = call_function(function_call, verbose)
                messages.append(function_response_content)
        else:
            print(response.text)
            return

    print(f"Warning: Reached maximum iteration limit ({max_iters}) without a final response.")


if __name__ == "__main__":
    main()
