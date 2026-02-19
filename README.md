# Pythonic Implementation of Basic Claude Code Clone

Claude Code is an AI coding assistant that uses Large Language Models (LLMs) to
understand code and perform actions through tool calls. In this challenge,
you'll build your own Claude Code from scratch by implementing an LLM-powered
coding assistant.

Along the way you'll learn about HTTP RESTful APIs, OpenAI-compatible tool
calling, agent loop, and how to integrate multiple tools into an AI assistant.

## Installation and Usage

1. Download Repo from GitHub.

   Using SSH:
   ```
   git clone git@github.com:tmooney84/codecrafters-claude-code-python.git
   ```

   ```
   Using HTTPS: https://github.com/tmooney84/codecrafters-claude-code-python.git
   ```

2. Navigate to Local Repo Directory.
   ``` 
   cd codecrafters-claude-code-python
   ```

3. Ensure you have `uv` installed locally.
   
4. If you do not already have an OpenRouter account and key, go to https://openrouter.ai/ and set up an account.

5. Once you have your API key temporarily set the global variable OPENROUTER_API_KEY to your key.
   ```
   export OPENROUTER_API_KEY="your_actual_api_key_here"
   ```

7. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
