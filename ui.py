import customtkinter as ctk
from tkinter import messagebox
import threading
from auth import GitHubAuthManager
from git_manager import MinecraftGitManager

class MineSyncUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MineSync - Synchronisation P2P Minecraft")
        self.geometry("900x650")
        
        self.auth_manager = GitHubAuthManager()
        self.git_manager = MinecraftGitManager(self.auth_manager.access_token)
        self.selected_world = None

        self.build_ui()
        self.check_initial_auth()

    def build_ui(self):
        # --- Sidebar (Authentification) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="⛏️ MineSync", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=25, padx=20)

        self.auth_card = ctk.CTkFrame(self.sidebar, fg_color=("gray85", "gray15"))
        self.auth_card.pack(pady=10, padx=15, fill="x")
        
        self.auth_status_lbl = ctk.CTkLabel(self.auth_card, text="Non connecté", text_color="#ff5555", font=ctk.CTkFont(weight="bold"))
        self.auth_status_lbl.pack(pady=10)

        self.auth_btn = ctk.CTkButton(self.sidebar, text="Lier Compte GitHub", command=self.handle_auth)
        self.auth_btn.pack(pady=10, padx=20, fill="x")

        # --- Main Content Section ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Scroller horizontal des mondes Minecraft détectés
        self.world_section = ctk.CTkFrame(self.main_content)
        self.world_section.pack(fill="x", pady=10)
        
        self.world_title = ctk.CTkLabel(self.world_section, text="Sélectionne un monde Minecraft :", font=ctk.CTkFont(size=16, weight="bold"))
        self.world_title.pack(anchor="w", padx=15, pady=5)

        self.worlds_scroll = ctk.CTkScrollableFrame(self.world_section, height=130, orientation="horizontal")
        self.worlds_scroll.pack(fill="x", padx=15, pady=10)
        self.refresh_worlds_list()

        # Zone d'actions du monde sélectionné
        self.dashboard_frame = ctk.CTkFrame(self.main_content)
        self.dashboard_frame.pack(fill="both", expand=True, pady=10)
        
        self.dash_title = ctk.CTkLabel(self.dashboard_frame, text="Aucun monde sélectionné", font=ctk.CTkFont(size=18, weight="bold"))
        self.dash_title.pack(pady=15)

        self.actions_layout = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.actions_layout.pack(fill="x", padx=20, pady=5)

        self.share_btn = ctk.CTkButton(self.actions_layout, text="📤 Partager l'état de mon monde", fg_color="#2eb85c", hover_color="#228a45", font=ctk.CTkFont(size=14, weight="bold"), command=self.share_action, state="disabled")
        self.share_btn.pack(side="left", expand=True, padx=10, ipady=8)

        self.sync_btn = ctk.CTkButton(self.actions_layout, text="🔄 Vérifier si mon monde est à jour", fg_color="#39f", hover_color="#0077e6", font=ctk.CTkFont(size=14, weight="bold"), command=self.sync_action, state="disabled")
        self.sync_btn.pack(side="right", expand=True, padx=10, ipady=8)

        # Colonnes inférieures : Invitations (gauche) & Timeline (droite)
        self.split_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.split_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.collab_frame = ctk.CTkFrame(self.split_frame, width=280)
        self.collab_frame.pack(side="left", fill="both", padx=5, expand=True)
        
        ctk.CTkLabel(self.collab_frame, text="👥 Inviter des Joueurs (P2P)", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.collab_entry = ctk.CTkEntry(self.collab_frame, placeholder_text="Pseudo GitHub de ton ami")
        self.collab_entry.pack(pady=5, padx=15, fill="x")
        self.collab_btn = ctk.CTkButton(self.collab_frame, text="Ajouter l'accès au monde", command=self.invite_friend, state="disabled")
        self.collab_btn.pack(pady=10, padx=15, fill="x")

        self.timeline_frame = ctk.CTkFrame(self.split_frame)
        self.timeline_frame.pack(side="right", fill="both", padx=5, expand=True)
        
        ctk.CTkLabel(self.timeline_frame, text="⏳ Historique & Voyage Temporel", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.timeline_scroll = ctk.CTkScrollableFrame(self.timeline_frame, height=150)
        self.timeline_scroll.pack(fill="both", expand=True, padx=15, pady=5)

    def check_initial_auth(self):
        if self.auth_manager.access_token:
            self.git_manager = MinecraftGitManager(self.auth_manager.access_token)
            try:
                username = self.git_manager.github_client.get_user().login
                self.auth_status_lbl.configure(text=f"Connecté : {username}", text_color="#2eb85c")
                self.auth_btn.configure(text="Déconnexion", fg_color="#e55353", hover_color="#c93b3b")
            except Exception:
                self.auth_manager.logout()

    def handle_auth(self):
        if self.auth_manager.access_token:
            self.auth_manager.logout()
            self.git_manager = MinecraftGitManager(None)
            self.auth_status_lbl.configure(text="Non connecté", text_color="#ff5555")
            self.auth_btn.configure(text="Lier Compte GitHub", fg_color=["#3a7ebf", "#1f538d"])
            self.toggle_world_buttons("disabled")
            messagebox.showinfo("Déconnexion", "Compte dissocié avec succès.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Liaison GitHub")
        popup.geometry("450x250")
        popup.transient(self)
        popup.grab_set()

        lbl_info = ctk.CTkLabel(popup, text="Génération du code de connexion...", font=ctk.CTkFont(size=14))
        lbl_info.pack(pady=30, padx=20)

        def update_popup_status(text, user_code=None, uri=None):
            if user_code:
                lbl_info.configure(text=f"1. Ton navigateur internet va s'ouvrir\n2. Saisis ce code de sécurité :\n\n {user_code} \n\nEn attente de validation sur GitHub...", font=ctk.CTkFont(size=14, weight="bold"))
            else:
                lbl_info.configure(text=text)

        def run_flow():
            token = self.auth_manager.start_device_flow(update_popup_status)
            if token:
                self.git_manager = MinecraftGitManager(token)
                username = self.git_manager.github_client.get_user().login
                self.auth_status_lbl.configure(text=f"Connecté : {username}", text_color="#2eb85c")
                self.auth_btn.configure(text="Déconnexion", fg_color="#e55353", hover_color="#c93b3b")
                self.refresh_worlds_list()
                popup.destroy()
                messagebox.showinfo("MineSync", f"Succès ! Bienvenue {username}.")
            else:
                popup.destroy()

        threading.Thread(target=run_flow, daemon=True).start()

    def refresh_worlds_list(self):
        for widget in self.worlds_scroll.winfo_children():
            widget.destroy()
        worlds = self.git_manager.list_local_worlds()
        if not worlds:
            ctk.CTkLabel(self.worlds_scroll, text="Aucun monde détecté dans .minecraft/saves").pack(pady=10)
            return
        for world in worlds:
            btn = ctk.CTkButton(self.worlds_scroll, text=f"🗺️ {world}", width=140, height=80, fg_color=("gray80", "gray20"), text_color=("black", "white"), hover_color=("gray70", "gray30"), command=lambda w=world: self.select_world(w))
            btn.pack(side="left", padx=10, pady=5)

    def select_world(self, world_name):
        self.selected_world = world_name
        self.dash_title.configure(text=f"Configuration de : {world_name}")
        if self.auth_manager.access_token:
            self.toggle_world_buttons("normal")
            threading.Thread(target=lambda: self.git_manager.init_or_load_repo(world_name), daemon=True).start()
            self.refresh_timeline()
        else:
            messagebox.showwarning("MineSync", "Liez votre compte GitHub d'abord.")

    def toggle_world_buttons(self, state):
        self.share_btn.configure(state=state)
        self.sync_btn.configure(state=state)
        self.collab_btn.configure(state=state)

    def share_action(self):
        self.share_btn.configure(text="⏳ Publication...", state="disabled")
        def run():
            try:
                self.git_manager.share_world(self.selected_world)
                messagebox.showinfo("Succès", "Sauvegarde partagée en ligne ! Vos amis peuvent se synchroniser.")
                self.refresh_timeline()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
            finally:
                self.share_btn.configure(text="📤 Partager l'état de mon monde", state="normal")
        threading.Thread(target=run, daemon=True).start()

    def sync_action(self):
        self.sync_btn.configure(text="⏳ Vérification...", state="disabled")
        def run():
            try:
                status = self.git_manager.check_and_update_world(self.selected_world)
                if status == "UP_TO_DATE":
                    messagebox.showinfo("MineSync", "Votre monde est déjà parfaitement à jour !")
                elif status == "UPDATED":
                    messagebox.showinfo("MineSync", "Mise à jour réussie ! Les données de vos amis ont été appliquées.")
                    self.refresh_timeline()
                elif status == "AHEAD":
                    messagebox.showinfo("MineSync", "Vous possédez des modifications non partagées. Cliquez sur 'Partager'.")
                elif status == "CONFLICT_DETECTED":
                    self.ask_conflict_resolution()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
            finally:
                self.sync_btn.configure(text="🔄 Vérifier si mon monde est à jour", state="normal")
        threading.Thread(target=run, daemon=True).start()

    def ask_conflict_resolution(self):
        """Interface explicite demandant quelle branche/version conserver"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚠️ Conflit détecté entre les sauvegardes !")
        dialog.geometry("500x320")
        dialog.transient(self)
        dialog.grab_set()

        lbl = ctk.CTkLabel(dialog, text="Oups ! Conflit de versions 🤯", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f5a623")
        lbl.pack(pady=15)

        txt = ("Toi et un autre joueur avez modifié le monde en même temps.\n"
               "Quelle version faut-il propager pour le groupe ?\n\n"
               "💡 Ta version actuelle a été sauvegardée dans une branche de secours.")
        lbl_txt = ctk.CTkLabel(dialog, text=txt, font=ctk.CTkFont(size=12), justify="center")
        lbl_txt.pack(pady=10, padx=20)

        def choose(option):
            self.git_manager.resolve_conflict(self.selected_world, option)
            dialog.destroy()
            messagebox.showinfo("Résolu", f"Le monde est aligné sur la version : {option}")
            self.refresh_timeline()

        btn_local = ctk.CTkButton(dialog, text="Garder MA version locale (Écrase le cloud)", fg_color="#e55353", hover_color="#c93b3b", command=lambda: choose("local"))
        btn_local.pack(fill="x", padx=40, pady=10, ipady=5)

        btn_remote = ctk.CTkButton(dialog, text="Garder la version EN LIGNE (Écrase mes fichiers)", fg_color="#2eb85c", hover_color="#228a45", command=lambda: choose("remote"))
        btn_remote.pack(fill="x", padx=40, pady=5, ipady=5)

    def refresh_timeline(self):
        for widget in self.timeline_scroll.winfo_children():
            widget.destroy()
        commits = self.git_manager.get_timeline(self.selected_world)
        if not commits:
            ctk.CTkLabel(self.timeline_scroll, text="Aucun historique.").pack(pady=10)
            return

        if len(commits) > 1:
            reset_btn = ctk.CTkButton(self.timeline_scroll, text="💥 Revenir à la toute première version (Reset)", fg_color="#df4759", hover_color="#b52b3a", command=lambda: self.trigger_rollback(commits[-1]["sha"]))
            reset_btn.pack(fill="x", padx=5, pady=5)

        for i, commit in enumerate(commits):
            card = ctk.CTkFrame(self.timeline_scroll, fg_color=("gray90", "gray25"))
            card.pack(fill="x", pady=4, padx=5)
            
            prefix = "⭐ Version Actuelle" if i == 0 else f"📦 Sauvegarde du {commit['date']}"
            lbl_title = ctk.CTkLabel(card, text=prefix, font=ctk.CTkFont(weight="bold", size=12))
            lbl_title.pack(anchor="w", padx=10, pady=2)

            if i > 0:
                rollback_btn = ctk.CTkButton(card, text="⏪ Restaurer", size=(80, 22), command=lambda s=commit["sha"]: self.trigger_rollback(s))
                rollback_btn.pack(anchor="e", padx=10, pady=5)

    def trigger_rollback(self, sha):
        if messagebox.askyesno("Rollback", "Restaurer cette ancienne version ? Vos changements actuels seront écrasés."):
            try:
                self.git_manager.rollback_to(self.selected_world, sha)
                messagebox.showinfo("Voyage réussi", "Monde restauré ! Relancez Minecraft.")
                self.refresh_timeline()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def invite_friend(self):
        friend = self.collab_entry.get().strip()
        if not friend: return
        try:
            self.git_manager.invite_collaborator(self.selected_world, friend)
            messagebox.showinfo("Invité !", f"{friend} a été ajouté au projet avec succès.")
            self.collab_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erreur", f"Pseudo introuvable ou erreur : {e}")