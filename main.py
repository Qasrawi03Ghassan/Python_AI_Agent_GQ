import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")    

def main():
    print("Hello from Python-AI-Agent-GQ!")

    if not api_key or api_key is None:
        raise RuntimeError("Could not get API key for GEMINI")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="User prompt")
    parser.add_argument("--verbose", action="store_true",help="Enable verbose output")
    args = parser.parse_args()

    messages_list:list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]


    response = client.models.generate_content(model="gemini-2.5-flash",contents=messages_list)

    metadata = response.usage_metadata
    if not metadata or metadata is None:
        raise RuntimeError("Couldn't access response's metadata due to an error")

    prompt_tokens = metadata.prompt_token_count
    response_tokens = metadata.candidates_token_count

    if args.verbose:
        print("User prompt: " + str(args.user_prompt))
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))

    print("Response:\n"+response.text)



if __name__ == "__main__":
    main()
