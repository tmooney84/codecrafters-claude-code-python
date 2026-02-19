import argparse
import os
import subprocess
import json
import sys
from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
IS_LOCAL = os.getenv("IS_LOCAL", False)

def bash(command: str)-> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
    

def read(file_path: str)-> str:
    with open(file_path, "r") as f:
        return f.read()

#Does this need to have a variable number of args instead? 
def write(file_path: str, content: str)-> None:
    with open(file_path, "w") as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"
    
TOOLS = {"bash": bash,
         "read": read,
         "write": write}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    messages = [{"role": "user", "content": args.p}]

    while True:
        chat = client.chat.completions.create(
            #model = "z-ai/glm-4.5-air:free",
            model ="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "bash",
                        "description": "Execute a shell command",
                        "parameters": {
                            "type": "object",
                            "required": ["command"],
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The command to execute"
                                }
                            },
                        },
                    },
                },

                {
                    "type": "function",
                    "function": {
                        "name": "read",
                        "description": "Read and return the contents of a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path to the file to read",
                                }
                            },
                            "required": ["file_path"],
                        },
                    },
                },

                {
                    "type": "function",
                    "function": {
                        "name": "write",
                        "description": "Write content to a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path of the file to write to",
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content to write to the file",
                                },
                            },
                        "required": ["file_path", "content"],
                        },
                    },
                },
            ],
        )
        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        message = chat.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls: 
                fn = tool_call.function
                function = fn.name
                function_name = function.lower()

                tool_args = json.loads(fn.arguments)

                result = TOOLS[function_name](**tool_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        if chat.choices[0].finish_reason == "stop":
            break

    print(chat.choices[0].message.content)




if __name__ == "__main__":
    main()
