import os
import platform
from datetime import datetime
from git import Repo, exc
from github import Github

class MinecraftGitManager:
    def __init__(self, token=None):
        self.token = token
        self.github_client = Github(token) if token else None
        self.saves_dir = self.get_minecraft_saves_dir()

    def get_minecraft_saves_dir(self):
        """Détecte l'emplacement natif du dossier de sauvegarde Minecraft par OS"""
        system = platform.system()
        if system == "Windows":
            path = os.path.join(os.environ.get("APPDATA", ""), ".minecraft", "saves")
        elif system == "Darwin": # macOS
            path = os.path.expanduser("~/Library/Application Support/minecraft/saves")
        else: # Linux
            path = os.path.expanduser("~/.minecraft/saves")
        return path if os.path.exists(path) else None

    def list_local_worlds(self):
        if not self.saves_dir or not os.path.exists(self.saves_dir):
            return []
        return [d for d in os.listdir(self.saves_dir) if os.path.isdir(os.path.join(self.saves_dir, d))]

    def get_repo_name(self, world_name):
        return f"mc-world-{world_name.lower().replace(' ', '-')}"

    def init_or_load_repo(self, world_name):
        world_path = os.path.join(self.saves_dir, world_name)
        
        # Initialisation Git Locale et création du .gitignore automatique
        try:
            repo = Repo(world_path)
        except exc.InvalidGitRepositoryError:
            repo = Repo.init(world_path)
            gitignore_path = os.path.join(world_path, ".gitignore")
            if not os.path.exists(gitignore_path):
                with open(gitignore_path, "w") as f:
                    f.write("session.lock\nlogs/\ncrash-reports/\ndebug/\n*.tmp\n")
            repo.git.add(".gitignore")
            repo.index.commit("Initialisation de MineSync (.gitignore)")

        # Normalisation du nom de la branche sur 'main'
        if 'main' not in repo.heads:
            if 'master' in repo.heads:
                repo.git.branch('-m', 'master', 'main')
            else:
                repo.git.checkout('-b', 'main')

        # Création ou liaison automatique du dépôt GitHub Privé
        if "origin" not in [r.name for r in repo.remotes] and self.github_client:
            user = self.github_client.get_user()
            repo_name = self.get_repo_name(world_name)
            
            try:
                gh_repo = user.get_repo(repo_name)
            except:
                gh_repo = user.create_repo(repo_name, private=True, description="Sauvegarde Minecraft MineSync")
            
            # Injection sécurisée du token pour éviter toute invite de commande système
            auth_url = gh_repo.clone_url.replace("https://", f"https://{self.token}@")
            repo.create_remote("origin", auth_url)
            
        return repo

    def share_world(self, world_name):
        """Publie les modifications locales vers GitHub"""
        repo = self.init_or_load_repo(world_name)
        repo.git.add(A=True)
        
        if repo.is_dirty(untracked_files=True):
            timestamp = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
            repo.index.commit(f"Mise à jour du monde - {timestamp}")
            
        origin = repo.remote(name="origin")
        origin.push(refspec="main:main")

    def check_and_update_world(self, world_name):
        """Analyse l'état distant et applique ou lève une alerte de conflit"""
        repo = self.init_or_load_repo(world_name)
        origin = repo.remote(name="origin")
        
        # Récupère l'état distant sans fusionner immédiatement
        origin.fetch()
        
        local_commit = repo.heads.main.commit
        remote_ref = "origin/main"
        if remote_ref not in [ref.name for ref in repo.references]:
            return "UP_TO_DATE"
            
        remote_commit = repo.references[remote_ref].commit

        if local_commit == remote_commit:
            return "UP_TO_DATE"

        # Recherche de l'ancêtre commun pour détecter la divergence
        base = repo.merge_base(local_commit, remote_commit)[0]
        
        if base == local_commit:
            # Fast-forward : On applique la mise à jour distante proprement
            repo.git.read_tree('-m', '-u', remote_commit)
            repo.head.reference = repo.references[remote_ref]
            repo.head.reset(index=True, working_tree=True)
            return "UPDATED"
        elif base == remote_commit:
            # En avance localement
            return "AHEAD"
        else:
            # CONFLIT DÉTECTÉ (Deux personnes ont joué séparément)
            # Sauvegarde de secours immédiate de la version locale sur une branche datée
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            repo.create_head(f"conflit-local-{timestamp}")
            return "CONFLICT_DETECTED"

    def resolve_conflict(self, world_name, choice):
        """Résolution définitive selon le bouton cliqué par l'utilisateur"""
        repo = self.init_or_load_repo(world_name)
        if choice == "local":
            # On force notre version locale à écraser GitHub (Force Push)
            repo.remote(name="origin").push(refspec="main:main", force=True)
        elif choice == "remote":
            # On force la version de GitHub à écraser notre dossier local (Hard Reset)
            repo.git.reset("--hard", "origin/main")

    def get_timeline(self, world_name):
        """Génère l'historique complet pour la frise chronologique graphique"""
        try:
            repo = self.init_or_load_repo(world_name)
            commits = []
            for commit in repo.iter_commits('main'):
                commits.append({
                    "sha": commit.hexsha,
                    "message": commit.message.strip(),
                    "date": datetime.fromtimestamp(commit.committed_date).strftime("%d/%m/%Y %H:%M")
                })
            return commits
        except Exception:
            return []

    def rollback_to(self, world_name, sha):
        repo = self.init_or_load_repo(world_name)
        repo.git.reset("--hard", sha)

    def invite_collaborator(self, world_name, github_username):
        if not self.github_client:
            raise Exception("Non connecté à GitHub")
        user = self.github_client.get_user()
        repo_name = self.get_repo_name(world_name)
        gh_repo = user.get_repo(repo_name)
        gh_repo.add_to_collaborators(github_username, permission="push")