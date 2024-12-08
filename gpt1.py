import os
import sys
import openai
import time
import threading
from colorama import Fore, Style, init
import requests.exceptions

# Initialize colorama
init(autoreset=True)

# Define a simple loading animation
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\r{Fore.YELLOW}Fetching response... {animation[idx % len(animation)]}{Style.RESET_ALL}", end="")
        idx += 1
        time.sleep(0.1)

def fetch_response_with_retry(conversation_history, retries=2, timeout=13):
    for attempt in range(retries + 1):  # Initial attempt + retries
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        try:
            # Start the loading animation
            loading_thread.start()

            # Time-limited API request
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=conversation_history,
                temperature=0.7,
                max_tokens=1000,
                request_timeout=timeout  # Explicit timeout parameter
            )
            return response.choices[0].message.content.strip()
        except openai.error.Timeout as e:
            print(f"{Fore.RED}Request timed out: {e}. Retrying... ({attempt + 1}/{retries}){Style.RESET_ALL}")
        except requests.exceptions.Timeout as e:
            print(f"{Fore.RED}Connection timeout: {e}. Retrying... ({attempt + 1}/{retries}){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}. Retrying... ({attempt + 1}/{retries}){Style.RESET_ALL}")
        finally:
            stop_event.set()
            loading_thread.join()
            print("\r", end="")  # Clear the loading line

        if attempt == retries:  # If the last attempt fails
            raise Exception("Failed to fetch response after multiple attempts.")

def main():
    # Ensure the API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}Error: OPENAI_API_KEY environment variable not set.{Style.RESET_ALL}")
        sys.exit(1)
    openai.api_key = api_key

    # Check if the user has provided an initial prompt
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Usage: ./chatgpt_cli.py 'Your prompt here'{Style.RESET_ALL}")
        sys.exit(1)

    # Join all command-line arguments into one initial prompt string
    user_prompt = " ".join(sys.argv[1:])

    # Initialize the conversation history
    conversation_history = [{"role": "user", "content": user_prompt}]

    # Display the initial user prompt
    print(f"{Fore.GREEN}You: {user_prompt}{Style.RESET_ALL}")

    while True:
        try:
            # Fetch the AI's response with retry mechanism
            answer = fetch_response_with_retry(conversation_history)
            print(f"{Fore.CYAN}AI: {answer}{Style.RESET_ALL}")

            # Append the AI's response to the conversation history
            conversation_history.append({"role": "assistant", "content": answer})

            # Ask the user for a follow-up question or allow them to exit
            follow_up = input(f"{Fore.GREEN}\nYou: {Style.RESET_ALL}")
            if follow_up.lower() in ["exit", "quit", "q"]:
                print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                break

            # Append the user's follow-up to the conversation history
            conversation_history.append({"role": "user", "content": follow_up})

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            sys.exit(1)

if __name__ == "__main__":
    main()
