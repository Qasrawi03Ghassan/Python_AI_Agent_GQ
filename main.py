import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_functions import available_functions,call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")    

def main():
    print("Hello from Python-AI-Agent-GQ!")
    print('\n')

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

    try:
         
        response = client.models.generate_content(model="gemini-2.5-flash",contents=messages_list,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt,temperature=0))
    except Exception as e:
         print(f'ERROR: gemini API error: {e}')
         return

    metadata = response.usage_metadata
    if not metadata or metadata is None:
        raise RuntimeError("Couldn't access response's metadata due to an error")

    prompt_tokens = metadata.prompt_token_count
    response_tokens = metadata.candidates_token_count

    if args.verbose:
        print("User prompt: " + str(args.user_prompt))
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))

    function_responses = []
    if response.function_calls is None:
        print("Response:\n"+response.text)

    else:
                for function_call in response.function_calls:
                    #print(f"Calling function: {function_call.name}({function_call.args})")

                    function_call_result = call_function(function_call=function_call,verbose=args.verbose)
                    if function_call_result.parts is None:
                        raise Exception(f'function_call_result doesn\'t have parts list')
                    
                    if function_call_result.parts[0].function_response is None:
                         raise Exception(f'function_call_result.parts[0].function_response is none')
                    
                    if function_call_result.parts[0].function_response.response is None:
                         raise Exception(f'function_call_result.parts[0].function_response.response is none')
                    
                    function_responses.append(function_call_result.parts[0])
                    if args.verbose:
                         print(f"-> {function_call_result.parts[0].function_response.response}")
                    else:
                         print(function_call_result.parts[0].function_response.response)
                         
            



if __name__ == "__main__":
    main()
