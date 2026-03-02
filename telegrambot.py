import os
from telegram import Bot
import asyncio

# Initialisation du bot Telegram
TOKEN = os.environ.get('TOKEN')
CHANNEL = os.environ.get('CHANNEL')

if not TOKEN or not CHANNEL:
    print("[X] Erreur: TOKEN et CHANNEL doivent être définis")
    exit(1)

bot = Bot(token=TOKEN)

def sendMessage(text):
    """Envoie un message texte sur Telegram"""
    try:
        print(f"[I] Envoi à Telegram: {text[:50]}...")
        
        # Créer une boucle asyncio pour envoyer le message
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.send_message(chat_id=CHANNEL, text=text))
        loop.close()
        
        print("[I] Message envoyé avec succès")
        return True
    except Exception as e:
        print(f"[X] Erreur d'envoi Telegram: {e}")
        return False
