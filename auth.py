import requests
import time
import webbrowser
import os
from config import GITHUB_CLIENT_ID, KEYRING_SERVICE, KEYRING_ACCOUNT  #, TOKEN_FILE
import keyring
from keyring.errors import PasswordDeleteError


class GitHubAuthManager:
    def __init__(self):
        self.client_id = GITHUB_CLIENT_ID
        self.access_token = self.load_cached_token()

    # def load_cached_token(self):
    #     if os.path.exists(TOKEN_FILE):
    #         with open(TOKEN_FILE, "r") as f:
    #             return f.read().strip()
    #     return None

    # def save_token(self, token):
    #     self.access_token = token
    #     with open(TOKEN_FILE, "w") as f:
    #         f.write(token)

    # def logout(self):
    #     self.access_token = None
    #     if os.path.exists(TOKEN_FILE):
    #         os.remove(TOKEN_FILE)

    def load_cached_token(self):
        """Récupère le token de manière sécurisée depuis le coffre-fort du système"""
        try:
            return keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
        except Exception:
            return None

    def save_token(self, token):
        """Chiffre et sauvegarde le token dans le coffre-fort du système"""
        self.access_token = token
        try:
            keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, token)
        except Exception as e:
            print(f"Impossible de sauvegarder le token dans le keyring : {e}")

    def logout(self):
        """Efface proprement le token de la mémoire et du système"""
        self.access_token = None
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
        except (PasswordDeleteError, Exception):
            # Le token n'existait pas ou a déjà été supprimé, on ignore l'erreur
            pass

    def start_device_flow(self, status_callback):
        """Lance la procédure d'authentification par code appareil sans Token manuel"""
        url = "https://github.com/login/device/code"
        headers = {"Accept": "application/json"}
        payload = {"client_id": self.client_id, "scope": "repo,user"}

        try:
            response = requests.post(url, headers=headers, data=payload).json()
            device_code = response.get("device_code")
            user_code = response.get("user_code")
            verification_uri = response.get("verification_uri")
            interval = response.get("interval", 5)

            # Transmet les infos à l'UI pour affichage
            status_callback(f"Ouvre : {verification_uri}\nCode : {user_code}", user_code, verification_uri)
            
            # Ouvre automatiquement le navigateur par défaut
            webbrowser.open(verification_uri)

            # Boucle d'attente (Polling) de la validation utilisateur
            token_url = "https://github.com/login/oauth/access_token"
            token_payload = {
                "client_id": self.client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }

            while True:
                time.sleep(interval)
                token_res = requests.post(token_url, headers=headers, data=token_payload).json()
                
                if "access_token" in token_res:
                    token = token_res["access_token"]
                    self.save_token(token)
                    return token
                elif token_res.get("error") == "authorization_pending":
                    continue
                elif token_res.get("error") == "expired_token":
                    status_callback("Le code a expiré. Veuillez réessuyer.", None, None)
                    return None
                else:
                    status_callback(f"Erreur : {token_res.get('error_description')}", None, None)
                    return None
        except Exception as e:
            status_callback(f"Erreur de connexion : {e}", None, None)
            return None