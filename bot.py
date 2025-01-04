import os
from flask import Flask
from pyrogram import Client, filters
from haystack.nodes import FARMReader
from haystack.utils import fetch_archive_from_http

# Telegram bot setup
BOT_TOKEN = "7319716758:AAFoejp2N8CEdzkXEF-EsvVAJd-D_k8x_uo"
API_ID = "24673538"
API_HASH = "555639745e6ceee1ae3797866136998f"

# Flask setup
app = Flask(__name__)

# Initialize Pyrogram client (Telegram bot)
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize FARMReader for haystack search
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")

# A simple function to fetch documents (you can replace with actual document fetch logic)
def search_documents(query):
    document_texts = [
        "Document 1: This is about AI and machine learning.",
        "Document 2: Python programming is great for AI.",
        "Document 3: Search AI technology and its applications.",
        "Document 4: This document talks about machine learning models."
    ]
    results = [doc for doc in document_texts if query.lower() in doc.lower()]
    return results

# Command handler for searching documents (Telegram bot)
@bot.on_message(filters.command("search"))
async def search(client, message):
    query = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""
    
    if not query:
        await message.reply("Kripya apna search query dein.")
        return
    
    results = search_documents(query)
    
    if results:
        result_message = "\n\n".join(results)
        await message.reply(f"Search results:\n\n{result_message}")
    else:
        await message.reply("Koi results nahi mile.")

# Flask route to check if the app is running
@app.route('/')
def index():
    return "Flask app is running!"

# Start Flask and Telegram bot
if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    # Start Telegram bot
    bot.run()
