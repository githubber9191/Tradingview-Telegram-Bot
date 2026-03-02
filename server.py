from flask import Flask, request
import os
import telegrambot

app = Flask('')

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    try:
        if request.method == 'POST':
            # Récupérer le message (texte brut ou JSON)
            if request.is_json:
                data = request.get_json()
                message = data.get('message') or data.get('text') or str(data)
            else:
                message = request.get_data(as_text=True)
            
            # Nettoyer le message
            message = message.strip()
            
            print(f"[I] Message reçu: {message[:50]}...")
            
            # Envoyer à Telegram
            telegrambot.sendMessage(message)
            
            return 'success', 200
        else:
            # Requête GET (pour les tests)
            return 'Bot Telegram actif ! Utilise POST pour envoyer des messages.', 200
            
    except Exception as e:
        print(f"[X] Erreur: {e}")
        return 'error', 500

@app.route('/')
def home():
    return 'Bot Telegram opérationnel !'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
