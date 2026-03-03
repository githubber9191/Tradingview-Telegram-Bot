import os
import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')
CHANNEL = os.environ.get('CHANNEL')

if not TOKEN or not CHANNEL:
    logger.error("TOKEN ou CHANNEL manquant")
    exit(1)

bot = Bot(token=TOKEN)

async def send_async(text):
    """Fonction asynchrone interne"""
    return await bot.send_message(chat_id=CHANNEL, text=text)

def sendMessage(text):
    """Wrapper synchrone pour Flask"""
    try:
        logger.info(f"Tentative d'envoi: {text[:50]}...")
        
        # asyncio.run() crée une nouvelle boucle et la ferme proprement
        result = asyncio.run(send_async(text))
        
        if result and result.message_id:
            logger.info(f"✅ Message envoyé, ID: {result.message_id}")
            return True
        else:
            logger.error("❌ Pas de message_id")
            return False
            
    except TelegramError as e:
        logger.error(f"❌ Erreur Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return False
