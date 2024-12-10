# Advanced Therapy Bot

This is a Telegram bot designed to provide emotional support and therapy-like conversations with a friendly and caring persona, "Grandma Aviva". The bot is powered by Google’s generative AI and is designed to interact in a warm, empathetic, and non-judgmental manner, offering a safe space for users to share their thoughts and feelings.

## Features

- **Conversational AI**: The bot uses Google’s Gemini Pro AI model for generating human-like responses to users' messages.
- **Personalized Interaction**: The bot is designed to talk in a natural, affectionate, and simple tone, resembling the voice of a caring grandmother.
- **Emotionally Supportive**: It provides support for individuals seeking someone to listen and talk to, especially during tough times.
- **Context-Aware**: The bot remembers the last few exchanges in the conversation, enabling context-aware responses.
- **User-Friendly Commands**: 
  - `/start` - Starts a new conversation.
  - `/help` - Displays instructions on how to use the bot.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/buzagloidan/savta.git
    cd savta
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    You will need to set the following environment variables in a `.env` file:
    - `TELEGRAM_TOKEN`: Your Telegram Bot API token (obtainable from @BotFather on Telegram).
    - `GOOGLE_API_KEY`: Your Google API key for generative AI (Obtainable from Google Cloud).

    Example `.env` file:
    ```
    TELEGRAM_TOKEN=your-telegram-bot-token
    GOOGLE_API_KEY=your-google-api-key
    ```

4. **Run the bot:**

    ```bash
    python bot.py
    ```

## Usage

Once the bot is running, you can interact with it via Telegram by typing messages. It will respond based on your input in a supportive and caring manner.

- To start a conversation, type `/start`.
- To get instructions on how to use the bot, type `/help`.

## Safety Features

The bot uses advanced safety settings to prevent harmful content. It blocks inappropriate responses related to harassment, hate speech, sexually explicit content, and dangerous content.

## Notes

- This bot is for emotional support and should not be used as a replacement for professional therapy.
- In case of severe emotional distress, it is always recommended to contact a mental health professional or reach out to a crisis support helpline (e.g., Mental Health Crisis Helpline: 1201).
- All conversations are kept private and secure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google’s Gemini Pro AI for generative responses.
- Telegram API for providing the platform to interact with users.
