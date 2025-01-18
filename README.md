# CLI Conversation Tool

This is a simple command-line tool that interacts with a text generation service using an API. You can prompt it with questions or messages, and it will provide responses in a conversational manner.

## Features

- Command-line interface for interactive conversations.
- Retry mechanism for network or timeout issues.
- Color-coded output for better readability.

## Prerequisites

- Python 3.7 or higher.

## Installation

1. Clone this repository or download the script.
2. Navigate to the folder containing the script.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Obtain your API key from the text generation service provider.
2. Set the environment variable for your API key:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   (On Windows, use `set OPENAI_API_KEY="your_api_key_here"`)

## Usage

1. Open your terminal in the folder with the script.
2. Run the script with your initial prompt as an argument:
   ```bash
   python chatgpt_cli.py "Hello there!"
   ```
3. Type follow-up messages as needed. Enter `exit`, `quit`, or `q` to end the conversation.

Example session:
```
$ python chatgpt_cli.py "Tell me a story about a brave knight."
You: Tell me a story about a brave knight.

Fetching response... /
AI: Once upon a time, a knight set forth on a quest...
You: How about a story with a dragon?
AI: In another kingdom, a dragon lived atop a mountain...
You: quit
Goodbye!
```

**Note:** Replace `"Tell me a story about a brave knight."` with any text you want to explore or ask.

## Troubleshooting

- Make sure your environment variable `OPENAI_API_KEY` is correctly set.
- Check your internet connection if you encounter repeated timeout errors.
- The script automatically retries if it encounters a network or timeout issue.
