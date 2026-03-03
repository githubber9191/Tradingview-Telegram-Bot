from flask import Flask, request
import os
import logging
import telegrambot

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """Reçoit les alertes et les envoie à Telegram"""
    
    # Pour les requêtes GET (tests UptimeRobot)
    if request.method == 'GET':
        return "Bot actif", 200
    
    logger.info("=" * 50)
    logger.info("🔔 NOUVELLE ALERTE RECUE")
    logger.info(f"Headers: {dict(request.headers)}")
    
    try:
        # Récupérer les données
        if request.is_json:
            data = request.get_json()
            message = data.get('message') or data.get('text') or str(data)
            logger.info(f"Format: JSON, contenu: {message[:100]}")
        else:
            message = request.get_data(as_text=True).strip()
            logger.info(f"Format: Texte brut, contenu: {message[:100]}")
        
        if not message:
            message = "Alerte TradingView (message vide)"
            logger.warning("Message vide reçu")
        
        # Envoyer à Telegram et VÉRIFIER le résultat
        logger.info("📤 Envoi à Telegram...")
        success = telegrambot.sendMessage(message)
        
        if success:
            logger.info("✅ Message envoyé avec succès à Telegram")
            return 'success', 200
        else:
            logger.error("❌ ÉCHEC de l'envoi à Telegram")
            return 'error', 500  # ← Important : on retourne une erreur !
            
    except Exception as e:
        logger.exception(f"💥 Exception: {e}")
        return 'error', 500

@app.route('/')
def home():
    return 'Bot Telegram opérationnel', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Démarrage sur port {port}")
    app.run(host='0.0.0.0', port=port)
