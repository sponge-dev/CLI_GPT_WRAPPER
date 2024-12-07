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

    # Check if the user has provided an initial prompt
    if len(sys.argv) < 2:
        print("Usage: ./chatgpt_cli.py 'Your prompt here'")
        sys.exit(1)

    # Join all command-line arguments into one initial prompt string
    user_prompt = " ".join(sys.argv[1:])

    # Initialize the conversation history
    conversation_history = [{"role": "user", "content": user_prompt}]

    while True:
        try:
            # Create a chat completion using the conversation history
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=conversation_history,
                temperature=0.7,
                max_tokens=512
            )

            # The response content is in response.choices[0].message.content
            answer = response.choices[0].message.content.strip()
            print(f"AI: {answer}")

            # Append the AI's response to the conversation history
            conversation_history.append({"role": "assistant", "content": answer})

            # Ask the user for a follow-up question or allow them to exit
            follow_up = input("\nYou: ")
            if follow_up.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            # Append the user's follow-up to the conversation history
            conversation_history.append({"role": "user", "content": follow_up})

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
