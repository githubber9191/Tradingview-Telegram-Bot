import os
from telegram import Bot
import asyncio
import logging

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')
CHANNEL = os.environ.get('CHANNEL')

if not TOKEN or not CHANNEL:
    logger.error("TOKEN ou CHANNEL manquant")
    exit(1)

bot = Bot(token=TOKEN)

def sendMessage(text):
    """Envoie un message et retourne True/False selon le résultat"""
    try:
        logger.info(f"Tentative d'envoi: {text[:50]}...")
        
        # Créer une boucle asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Envoyer et attendre le résultat
        result = loop.run_until_complete(bot.send_message(
            chat_id=CHANNEL, 
            text=text
        ))
        loop.close()
        
        if result and result.message_id:
            logger.info(f"✅ Message envoyé, ID: {result.message_id}")
            return True
        else:
            logger.error("❌ Pas de message_id dans la réponse")
            return False
            
    except Exception as e:
        logger.error(f"❌ Exception Telegram: {e}")
        return False
