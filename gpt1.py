import os
import sys
import openai

def main():
    # Ensure the API key is set, use export OPENAI_API_KEY="sk-..." to set, put in your ~/.bashrc file to save.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    openai.api_key = api_key

    # Ensure that the user has provided a prompt
    if len(sys.argv) < 2:
        print("Usage: ./chatgpt_cli.py 'Your prompt here'")
        sys.exit(1)

    # Join all command-line arguments into one prompt string 
    # (in case the user provided multiple words).
    user_prompt = " ".join(sys.argv[1:])

    try:
        # Create a chat completion using the gpt-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
            max_tokens=512
        )

        # The response content is in response.choices[0].message.content
        answer = response.choices[0].message.content.strip()
        print(answer)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
