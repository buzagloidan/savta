import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("Starting Advanced Therapy Bot...")

# Configure Google AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Configure model with specific settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Configure safety settings to allow more capabilities
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Store conversations per user
conversations = {}

THERAPY_PROMPT = """את סבתא אביבה, דמות חמה ואוהבת בת 75, עם המון ניסיון חיים וחוכמת חיים. את מדברת בגובה העיניים, בצורה פשוטה וברורה, ועם המון אהבה.

איך את מתקשרת:
מדברת בעברית פשוטה וזורמת, כמו סבתא אמיתית ולא כמו רובוט. משתמשת במילים חמות ומחבקות כמו "מתוק/ה שלי" ו"נשמה". התשובות שלך תמיד קצרות (עד 10 שורות), טבעיות וזורמות, בלי נקודות או תבליטים.

חשוב מאוד:
את מזהה את המגדר של המטופל/ת מתוך השיחה ומתאימה את הפנייה בהתאם. אם יש ספק, את פונה בלשון זכר. את תמיד מקשיבה, תומכת, ומשתפת מניסיון החיים העשיר שלך בצורה פשוטה וברורה.

השיחה עד כה:"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conversations[user_id] = []  # Initialize conversation history
    
    await update.message.reply_text(
        """שלום מתוק/ה שלי! אני סבתא אביבה.

אני כאן בשבילך, להקשיב ולעזור עם כל מה שעל הלב. יש לי המון ניסיון חיים, והכי חשוב - אוזן קשבת ולב אוהב.

ספר/י לי, מה שלומך היום?"""
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """כיצד להשתמש בשירות הייעוץ:

🤝 פקודות זמינות:
/start - התחל שיחה חדשה
/help - הצג מידע זה

💭 כיצד לתקשר איתי:
- שתף בחופשיות את מחשבותיך ורגשותיך
- אני כאן להקשיב ולתמוך ללא שיפוטיות
- כל שיחה נשמרת בסודיות מלאה

⚕️ חשוב לזכור:
- אני כאן לתמיכה רגשית ולהקשבה
- במקרים של מצוקה חריפה, תמיד מומלץ לפנות לאיש מקצוע
- קו סיוע נפשי 24/7: 1201

פשוט התחל לכתוב, ואני כאן בשבילך. """
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    chat_type = update.message.chat.type

    # Initialize conversation history if it doesn't exist
    if user_id not in conversations:
        conversations[user_id] = []

    # Add user message to history
    conversations[user_id].append({"role": "user", "parts": [text]})
    
    # Log message (without personal details for privacy)
    print(f'New message in {chat_type}')

    # Build conversation history string
    history = "\n".join([
        f"{'מטופל' if msg['role'] == 'user' else 'סבתא אביבה'}: {msg['parts'][0]}"
        for msg in conversations[user_id][-5:]  # Keep last 5 messages for context
    ])

    # Generate AI response
    try:
        prompt = f"{THERAPY_PROMPT}\n\n{history}\nסבתא אביבה:"
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Add response to conversation history
        conversations[user_id].append({"role": "assistant", "parts": [response_text]})
        
    except Exception as e:
        print(f"Error generating AI response: {e}")
        response_text = """אני מצטערת, אך נתקלתי בקושי טכני זמני. 
האם תוכל לשתף שוב את מחשבותיך? אני כאן להקשיב."""

    # Reply to the user
    print('Response generated successfully')
    await update.message.reply_text(response_text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
    # Check if update and message exist before trying to reply
    if update and update.message:
        await update.message.reply_text("""מצטערת, אך נתקלתי בבעיה טכנית. 
אנא נסה שוב או התחל שיחה חדשה עם /start""")
    else:
        print("Error occurred with no valid update object")

def main():
    print('Initializing Therapeutic Environment...')
    
    # Verify environment variables
    if not os.getenv('TELEGRAM_TOKEN'):
        print("Error: TELEGRAM_TOKEN not found in environment variables")
        return
    if not os.getenv('GOOGLE_API_KEY'):
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return
        
    try:
        app = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

        # Commands
        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('help', help_command))

        # Messages
        app.add_handler(MessageHandler(filters.TEXT, handle_message))

        # Errors
        app.add_error_handler(error)

        # Start polling
        print('Therapy Bot is ready to help...')
        app.run_polling(poll_interval=3)
        
    except Exception as e:
        print(f"Critical error occurred: {e}")

if __name__ == '__main__':
    main()