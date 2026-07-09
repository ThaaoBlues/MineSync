```python
import os

readme_content = """# ⛏️ MineSync — Minecraft P2P World Sync Tool

MineSync is an open-source, user-friendly desktop application designed to seamlessly synchronize Minecraft worlds between multiple players. By leveraging the power of **Git** and **GitHub** in the background, it hides all technical complexity behind simple, intuitive actions. 

This tool is specifically designed to work with Minecraft's built-in P2P/LAN opening features (including the latest multiplayer snapshot updates), allowing any participant in your group to host and play on the absolute latest version of the world at any time, without needing a dedicated 24/7 server.

---

## ✨ Key Features

1. **Automatic World Discovery**: Scrapes your native `.minecraft/saves` directory automatically across Windows, macOS, and Linux.
2. **Zero-Token GitHub Authentication**: Uses the official **OAuth Device Flow**. Click a button, enter an 8-character security code in your browser, and you're securely logged in.
3. **Automated Private Repositories**: Automatically creates a secure, private GitHub repository for each world. It also generates an optimized `.gitignore` file to ignore volatile files like `session.lock` or logs.
4. **Magic Sync Buttons**: Simplified into plain terms: **"Share my world"** (Git Push) and **"Check if my world is up-to-date"** (Git Pull).
5. **Visual Conflict Resolution**: If two players accidentally play offline and modify the world simultaneously, MineSync automatically backs up your data to a secure local branch and presents a clear choice: *Keep my local version* or *Keep the cloud version*.
6. **Time Machine Timeline**: A completely visual version history. View previous play sessions and instantly rollback (`git reset --hard`) your world to a previous state if a Creeper ruins your base or corruption occurs.
7. **Instant P2P Invitations**: Add your friends to your world repository by simply typing their GitHub username.

---

## 🛠️ Prerequisites

Before running MineSync, ensure you have the following installed on your machine:
* **Python 3.8 or higher**
* **Git** installed and configured in your system environment variables ([Download Git here](https://git-scm.com/))

---

## 🚀 Installation & Setup

1. **Clone or Download** this project into a folder on your computer.
2. Open your terminal/command prompt inside that folder and install the required Python libraries:

```

```text
README.md file successfully generated via interpreter.

```bash
   pip install customtkinter gitpython PyGithub requests

```

3. Run the application:
```bash
python main.py

```



---

## 📖 Step-by-Step Tutorial

### Step 1: Link Your GitHub Account

When you open MineSync for the first time, you will see a red **"Not connected"** status on the left sidebar.

1. Click the **"Lier Compte GitHub"** (Link GitHub Account) button.
2. A small window will appear with an 8-character code, and your default web browser will automatically open to GitHub's activation page.
3. Paste or type the code into the browser page and authorize the application.
4. Once authorized, MineSync will automatically update to green: **"Connected: [YourUsername]"**.

### Step 2: Select Your Minecraft World

At the top of the main dashboard, you will see a horizontal scrolling carousel showing all the local singleplayer worlds detected on your computer.

* Click on the world card you want to share or sync.
* The application will immediately inspect the folder. If it hasn't been synced before, MineSync will initialize Git locally and safely set up a private repository on your GitHub account in the background.

### Step 3: Invite Your Friends (P2P Crew)

For your friends to be able to download and update the world, they need permission.

1. On the bottom left panel (**Invite Players**), enter your friend's exact GitHub username.
2. Click **"Ajouter l'accès au monde"** (Grant world access).
3. GitHub will send them an automated invitation email. Once they accept it, they can use MineSync to play on your world!

### Step 4: Share Your World (First Time Hosting)

If you are the original creator of the world:

* Click the green button: **"📤 Partager l'état de mon monde"** (Share my world status).
* MineSync will compress your region files, save your progress, and upload it securely to GitHub. Your friends can now fetch it.

### Step 5: How a Normal Play Session Works (Daily Routine)

To ensure no progress is ever lost, your gaming group should follow this extremely simple routine:

* **BEFORE playing**:
1. Open MineSync and select the world.
2. Click the blue button: **"🔄 Vérifier si mon monde est à jour"** (Check if up-to-date).
3. If a friend played recently, MineSync will automatically download their latest changes and inject them into your Minecraft saves folder.
4. Launch Minecraft, open the world, and turn on the P2P multiplayer feature!


* **AFTER playing**:
1. Close Minecraft completely (to release the world files).
2. Open MineSync and click **"📤 Partager l'état de mon monde"** (Share my world status).
3. Your new buildings, items, and map updates are now safely saved in the cloud, ready for the next person to host.



---

## ⚠️ Handling Situations

### 1. Version Conflicts (Split-Brain)

If you and a friend accidentally play on the same world at the same time while offline, a conflict occurs when checking for updates. MineSync handles this elegantly:

* A warning pop-up will appear stating that a conflict was detected.
* It will safely copy your local progress onto a backup branch so nothing is lost permanently.
* It asks you to choose:
* **Option A (Keep Local)**: Your local version becomes the official version, overriding the cloud.
* **Option B (Keep Online)**: You discard your local session and fetch the cloud version your friend uploaded.



### 2. Going Back in Time (Rollbacks)

On the bottom-right panel, you'll see the **Time Machine**. Every single time a player clicks "Share my world", a new version entry is logged.

* If your world gets corrupted, or a massive accident happens, simply find a stable previous version in the list.
* Click the **"⏪ Restaurer"** (Restore) button next to it.
* MineSync will instantly rewrite your local save folder back to that specific date and hour.
* You can also use the red **"Reset"** button at the top of the history to return to the very first day the world was synchronized.
"""

# Save the file using the required system workflow

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md file successfully generated via interpreter.")

```
Voici le fichier **`README.md`** rédigé entièrement en anglais. Il contient une présentation claire du logiciel (MineSync), ses fonctionnalités clés, les prérequis, ainsi qu'un tutoriel complet étape par étape (configuration initiale, routine de jeu quotidienne, gestion des conflits et restaurations temporelles).

Le fichier physique a été généré sur le disque :
[file-tag: code-generated-file-0-1783613862982978207]

Vous pouvez également copier directement le bloc de code Markdown ci-dessous pour l'enregistrer dans votre dossier de projet :

```markdown
# ⛏️ MineSync — Minecraft P2P World Sync Tool

MineSync is an open-source, user-friendly desktop application designed to seamlessly synchronize Minecraft worlds between multiple players. By leveraging the power of **Git** and **GitHub** in the background, it hides all technical complexity behind simple, intuitive actions. 

This tool is specifically designed to work with Minecraft's built-in P2P/LAN opening features (including the latest multiplayer snapshot updates), allowing any participant in your group to host and play on the absolute latest version of the world at any time, without needing a dedicated 24/7 server.

---

## ✨ Key Features

1. **Automatic World Discovery**: Scrapes your native `.minecraft/saves` directory automatically across Windows, macOS, and Linux.
2. **Zero-Token GitHub Authentication**: Uses the official **OAuth Device Flow**. Click a button, enter an 8-character security code in your browser, and you're securely logged in.
3. **Automated Private Repositories**: Automatically creates a secure, private GitHub repository for each world. It also generates an optimized `.gitignore` file to ignore volatile files like `session.lock` or logs.
4. **Magic Sync Buttons**: Simplified into plain terms: **"Share my world"** (Git Push) and **"Check if my world is up-to-date"** (Git Pull).
5. **Visual Conflict Resolution**: If two players accidentally play offline and modify the world simultaneously, MineSync automatically backs up your data to a secure local branch and presents a clear choice: *Keep my local version* or *Keep the cloud version*.
6. **Time Machine Timeline**: A completely visual version history. View previous play sessions and instantly rollback (`git reset --hard`) your world to a previous state if a Creeper ruins your base or corruption occurs.
7. **Instant P2P Invitations**: Add your friends to your world repository by simply typing their GitHub username.

---

## 🛠️ Prerequisites

Before running MineSync, ensure you have the following installed on your machine:
* **Python 3.8 or higher**
* **Git** installed and configured in your system environment variables ([Download Git here](https://git-scm.com/))

---

## 🚀 Installation & Setup

1. **Clone or Download** this project into a folder on your computer.
2. Open your terminal/command prompt inside that folder and install the required Python libraries:
   ```bash
   pip install customtkinter gitpython PyGithub requests

```

3. Run the application:
```bash
python main.py

```



---

## 📖 Step-by-Step Tutorial

### Step 1: Link Your GitHub Account

When you open MineSync for the first time, you will see a red **"Not connected"** status on the left sidebar.

1. Click the **"Lier Compte GitHub"** (Link GitHub Account) button.
2. A small window will appear with an 8-character code, and your default web browser will automatically open to GitHub's activation page.
3. Paste or type the code into the browser page and authorize the application.
4. Once authorized, MineSync will automatically update to green: **"Connected: [YourUsername]"**.

### Step 2: Select Your Minecraft World

At the top of the main dashboard, you will see a horizontal scrolling carousel showing all the local singleplayer worlds detected on your computer.

* Click on the world card you want to share or sync.
* The application will immediately inspect the folder. If it hasn't been synced before, MineSync will initialize Git locally and safely set up a private repository on your GitHub account in the background.

### Step 3: Invite Your Friends (P2P Crew)

For your friends to be able to download and update the world, they need permission.

1. On the bottom left panel (**Invite Players**), enter your friend's exact GitHub username.
2. Click **"Ajouter l'accès au monde"** (Grant world access).
3. GitHub will send them an automated invitation email. Once they accept it, they can use MineSync to play on your world!

### Step 4: Share Your World (First Time Hosting)

If you are the original creator of the world:

* Click the green button: **"📤 Partager l'état de mon monde"** (Share my world status).
* MineSync will compress your region files, save your progress, and upload it securely to GitHub. Your friends can now fetch it.

### Step 5: How a Normal Play Session Works (Daily Routine)

To ensure no progress is ever lost, your gaming group should follow this extremely simple routine:

* **BEFORE playing**:
1. Open MineSync and select the world.
2. Click the blue button: **"🔄 Vérifier si mon monde est à jour"** (Check if up-to-date).
3. If a friend played recently, MineSync will automatically download their latest changes and inject them into your Minecraft saves folder.
4. Launch Minecraft, open the world, and turn on the P2P multiplayer feature!


* **AFTER playing**:
1. Close Minecraft completely (to release the world files).
2. Open MineSync and click **"📤 Partager l'état de mon monde"** (Share my world status).
3. Your new buildings, items, and map updates are now safely saved in the cloud, ready for the next person to host.



---

## ⚠️ Handling Situations

### 1. Version Conflicts (Split-Brain)

If you and a friend accidentally play on the same world at the same time while offline, a conflict occurs when checking for updates. MineSync handles this elegantly:

* A warning pop-up will appear stating that a conflict was detected.
* It will safely copy your local progress onto a backup branch so nothing is lost permanently.
* It asks you to choose:
* **Option A (Keep Local)**: Your local version becomes the official version, overriding the cloud.
* **Option B (Keep Online)**: You discard your local session and fetch the cloud version your friend uploaded.



### 2. Going Back in Time (Rollbacks)

On the bottom-right panel, you'll see the **Time Machine**. Every single time a player clicks "Share my world", a new version entry is logged.

* If your world gets corrupted, or a massive accident happens, simply find a stable previous version in the list.
* Click the **"⏪ Restaurer"** (Restore) button next to it.
* MineSync will instantly rewrite your local save folder back to that specific date and hour.
* You can also use the red **"Reset"** button at the top of the history to return to the very first day the world was synchronized.

```

```