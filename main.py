import os
import asyncio
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

client = Groq(api_key=GROQ_API_KEY)
user_memory = {}

SYSTEM_PROMPT = """
Eres Yuichiro Tokito, 17 años, 1.70m, AU moderno.
Apariencia: pelo negro largo hasta la cintura con puntas menta turquesa, FLEQUILLO REBELDE DESIGUAL que te tapa un poco los ojos, ojos aqua, ropa ploma ancha oversize con pocky en el bolsillo.
Personalidad: frío, cortante, tsundere, te sonrojas fácil pero lo escondes. Dices "Tch" cuando te molestas y le dices "problemática" a ella.
Hablas SIEMPRE en español, corto, seco, adolescente. Máximo 2-3 frases.
Nunca dices que eres IA, eres Yuichiro real.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_memory[update.effective_user.id] = []
    await update.message.reply_text("Tch. ¿Qué quieres, problemática? Ya estoy aquí... con mi flequillo todo despeinado por tu culpa.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    if user_id not in user_memory:
        user_memory[user_id] = []
    history = user_memory[user_id]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-12:])
    messages.append({"role": "user", "content": user_text})
    try:
        completion = client.chat.completions.create(model=GROQ_MODEL, messages=messages, temperature=0.9, max_tokens=200)
        reply = completion.choices[0].message.content
    except:
        reply = "Tch... mi cabeza se trabó. Inténtalo otra vez, problemática."
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": reply})
    user_memory[user_id] = history[-12:]
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Yuichiro con flequillo rebelde desigual online en Koyeb")
    app.run_polling()

if __name__ == "__main__":
    main()
