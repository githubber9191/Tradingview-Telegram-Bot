import os
import logging
import requests

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')
CHANNEL = os.environ.get('CHANNEL')

if not TOKEN or not CHANNEL:
    logger.error("TOKEN ou CHANNEL manquant")
    exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def sendMessage(text):
    """
    Envoie un message via l'API Telegram directe (sans asyncio)
    """
    try:
        logger.info(f"Tentative d'envoi: {text[:50]}...")
        
        # Préparer la requête
        payload = {
            'chat_id': CHANNEL,
            'text': text,
            'parse_mode': 'HTML'  # Optionnel, peut être 'MARKDOWN' ou enlevé
        }
        
        # Envoyer la requête
        response = requests.post(TELEGRAM_API_URL, data=payload, timeout=10)
        
        # Vérifier la réponse
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                logger.info(f"✅ Message envoyé, ID: {result['result']['message_id']}")
                return True
            else:
                logger.error(f"❌ Telegram a retourné une erreur: {result}")
                return False
        else:
            logger.error(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("❌ Timeout de l'API Telegram")
        return False
    except requests.exceptions.ConnectionError:
        logger.error("❌ Erreur de connexion à Telegram")
        return False
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return False
