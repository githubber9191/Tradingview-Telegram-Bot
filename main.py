import server

if __name__ == '__main__':
    print("[I] Démarrage du bot Telegram...")
    server.app.run(host='0.0.0.0', port=5000)
