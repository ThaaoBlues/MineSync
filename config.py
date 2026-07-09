import os

# Identifiant de l'application OAuth GitHub (gère le Device Flow)
GITHUB_CLIENT_ID = "Ov23lisEDvPmteixIRPj"

# Fichier caché dans votre répertoire utilisateur pour mémoriser la connexion
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".minesync_token")


KEYRING_SERVICE = "MineSync_Minecraft_App"
KEYRING_ACCOUNT = "github_user_token"

import keyring
from keyring.errors import PasswordDeleteError