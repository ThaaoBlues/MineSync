import customtkinter as ctk
from tkinter import messagebox
import threading
from auth import GitHubAuthManager
from git_manager import MinecraftGitManager

class MineSyncUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MineSync - Minecraft P2P Synchronization")
        self.geometry("900x650")
        
        self.auth_manager = GitHubAuthManager()
        self.git_manager = MinecraftGitManager(self.auth_manager.access_token)
        self.selected_world = None

        self.build_ui()
        self.check_initial_auth()

    def build_ui(self):
        # --- Sidebar (Authentication) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="⛏️ MineSync", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=25, padx=20)

        self.auth_card = ctk.CTkFrame(self.sidebar, fg_color=("gray85", "gray15"))
        self.auth_card.pack(pady=10, padx=15, fill="x")
        
        self.auth_status_lbl = ctk.CTkLabel(self.auth_card, text="Not connected", text_color="#ff5555", font=ctk.CTkFont(weight="bold"))
        self.auth_status_lbl.pack(pady=10)

        self.auth_btn = ctk.CTkButton(self.sidebar, text="Link GitHub Account", command=self.handle_auth)
        self.auth_btn.pack(pady=10, padx=20, fill="x")

        # --- Main Content Section ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Horizontal slider for discovered Minecraft worlds
        self.world_section = ctk.CTkFrame(self.main_content)
        self.world_section.pack(fill="x", pady=10)
        
        self.world_title = ctk.CTkLabel(self.world_section, text="Select a Minecraft world:", font=ctk.CTkFont(size=16, weight="bold"))
        self.world_title.pack(anchor="w", padx=15, pady=5)

        self.worlds_scroll = ctk.CTkScrollableFrame(self.world_section, height=130, orientation="horizontal")
        self.worlds_scroll.pack(fill="x", padx=15, pady=10)
        self.refresh_worlds_list()

        # Selected world control dashboard
        self.dashboard_frame = ctk.CTkFrame(self.main_content)
        self.dashboard_frame.pack(fill="both", expand=True, pady=10)
        
        self.dash_title = ctk.CTkLabel(self.dashboard_frame, text="No world selected", font=ctk.CTkFont(size=18, weight="bold"))
        self.dash_title.pack(pady=15)

        self.actions_layout = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.actions_layout.pack(fill="x", padx=20, pady=5)

        self.share_btn = ctk.CTkButton(self.actions_layout, text="📤 Share my world status", fg_color="#2eb85c", hover_color="#228a45", font=ctk.CTkFont(size=14, weight="bold"), command=self.share_action, state="disabled")
        self.share_btn.pack(side="left", expand=True, padx=10, ipady=8)

        self.sync_btn = ctk.CTkButton(self.actions_layout, text="🔄 Check if my world is up-to-date", fg_color="#39f", hover_color="#0077e6", font=ctk.CTkFont(size=14, weight="bold"), command=self.sync_action, state="disabled")
        self.sync_btn.pack(side="right", expand=True, padx=10, ipady=8)

        # Bottom Columns: Invitations (Left) & Timeline History (Right)
        self.split_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.split_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.collab_frame = ctk.CTkFrame(self.split_frame, width=280)
        self.collab_frame.pack(side="left", fill="both", padx=5, expand=True)
        
        ctk.CTkLabel(self.collab_frame, text="👥 Invite Players (P2P Crew)", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.collab_entry = ctk.CTkEntry(self.collab_frame, placeholder_text="Friend's GitHub username")
        self.collab_entry.pack(pady=5, padx=15, fill="x")
        self.collab_btn = ctk.CTkButton(self.collab_frame, text="Grant world access", command=self.invite_friend, state="disabled")
        self.collab_btn.pack(pady=10, padx=15, fill="x")

        self.timeline_frame = ctk.CTkFrame(self.split_frame)
        self.timeline_frame.pack(side="right", fill="both", padx=5, expand=True)
        
        ctk.CTkLabel(self.timeline_frame, text="⏳ History & Time Machine", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.timeline_scroll = ctk.CTkScrollableFrame(self.timeline_frame, height=150)
        self.timeline_scroll.pack(fill="both", expand=True, padx=15, pady=5)

    def check_initial_auth(self):
        if self.auth_manager.access_token:
            self.git_manager = MinecraftGitManager(self.auth_manager.access_token)
            try:
                username = self.git_manager.github_client.get_user().login
                self.auth_status_lbl.configure(text=f"Connected: {username}", text_color="#2eb85c")
                self.auth_btn.configure(text="Disconnect", fg_color="#e55353", hover_color="#c93b3b")
            except Exception:
                self.auth_manager.logout()

    def handle_auth(self):
        if self.auth_manager.access_token:
            self.auth_manager.logout()
            self.git_manager = MinecraftGitManager(None)
            self.auth_status_lbl.configure(text="Not connected", text_color="#ff5555")
            self.auth_btn.configure(text="Link GitHub Account", fg_color=["#3a7ebf", "#1f538d"])
            self.toggle_world_buttons("disabled")
            messagebox.showinfo("Disconnect", "Account unlinked successfully.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("GitHub Link Activation")
        popup.geometry("460x280")
        popup.transient(self)
        popup.grab_set()

        lbl_info = ctk.CTkLabel(popup, text="Generating security login code...", font=ctk.CTkFont(size=14))
        lbl_info.pack(pady=20, padx=20)

        # Container layout for the selectable code entry box and copy button
        code_frame = ctk.CTkFrame(popup, fg_color="transparent")
        
        code_entry = ctk.CTkEntry(code_frame, width=160, justify="center", font=ctk.CTkFont(size=16, weight="bold"))
        code_entry.pack(side="left", padx=5)

        def copy_to_clipboard():
            self.clipboard_clear()
            self.clipboard_append(code_entry.get())
            # Briefly tweak the button appearance to show success feedback
            copy_btn.configure(text="✅ Copied!", fg_color="#2eb85c")
            self.after(1500, lambda: copy_btn.configure(text="📋 Copy Code", fg_color=["#3a7ebf", "#1f538d"]))

        copy_btn = ctk.CTkButton(code_frame, text="📋 Copy Code", width=100, command=copy_to_clipboard)
        copy_btn.pack(side="left", padx=5)

        lbl_status = ctk.CTkLabel(popup, text="", font=ctk.CTkFont(size=13, slant="italic"))
        lbl_status.pack(pady=15)

        def update_popup_status(text, user_code=None, uri=None):
            if user_code:
                lbl_info.configure(text="1. Your web browser will open automatically.\n2. Enter the following security code on GitHub:", font=ctk.CTkFont(size=13))
                code_frame.pack(pady=5)
                code_entry.configure(state="normal")
                code_entry.delete(0, "end")
                code_entry.insert(0, user_code)
                code_entry.configure(state="readonly") # Allows text selection, blocks text manual alteration
                lbl_status.configure(text="⏳ Awaiting validation from GitHub profile...", text_color="#39f")
            else:
                lbl_info.configure(text=text)
                code_frame.pack_forget()
                lbl_status.configure(text="")

        def run_flow():
            token = self.auth_manager.start_device_flow(update_popup_status)
            if token:
                self.git_manager = MinecraftGitManager(token)
                username = self.git_manager.github_client.get_user().login
                self.auth_status_lbl.configure(text=f"Connected: {username}", text_color="#2eb85c")
                self.auth_btn.configure(text="Disconnect", fg_color="#e55353", hover_color="#c93b3b")
                self.refresh_worlds_list()
                popup.destroy()
                messagebox.showinfo("MineSync", f"Success! Welcome {username}.")
            else:
                popup.destroy()

        threading.Thread(target=run_flow, daemon=True).start()

    def refresh_worlds_list(self):
        for widget in self.worlds_scroll.winfo_children():
            widget.destroy()
        worlds = self.git_manager.list_local_worlds()
        if not worlds:
            ctk.CTkLabel(self.worlds_scroll, text="No worlds detected inside .minecraft/saves directory").pack(pady=10)
            return
        for world in worlds:
            btn = ctk.CTkButton(self.worlds_scroll, text=f"🗺️ {world}", width=140, height=80, fg_color=("gray80", "gray20"), text_color=("black", "white"), hover_color=("gray70", "gray30"), command=lambda w=world: self.select_world(w))
            btn.pack(side="left", padx=10, pady=5)

    def select_world(self, world_name):
        self.selected_world = world_name
        self.dash_title.configure(text=f"Configuration for: {world_name}")
        if self.auth_manager.access_token:
            self.toggle_world_buttons("normal")
            threading.Thread(target=lambda: self.git_manager.init_or_load_repo(world_name), daemon=True).start()
            self.refresh_timeline()
        else:
            messagebox.showwarning("MineSync", "Please link your GitHub account first.")

    def toggle_world_buttons(self, state):
        self.share_btn.configure(state=state)
        self.sync_btn.configure(state=state)
        self.collab_btn.configure(state=state)

    def share_action(self):
        self.share_btn.configure(text="⏳ Publishing...", state="disabled")
        def run():
            try:
                self.git_manager.share_world(self.selected_world)
                messagebox.showinfo("Success", "World save shared online! Your friends can now sync up.")
                self.refresh_timeline()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.share_btn.configure(text="📤 Share my world status", state="normal")
        threading.Thread(target=run, daemon=True).start()

    def sync_action(self):
        self.sync_btn.configure(text="⏳ Checking...", state="disabled")
        def run():
            try:
                status = self.git_manager.check_and_update_world(self.selected_world)
                if status == "UP_TO_DATE":
                    messagebox.showinfo("MineSync", "Your local world save is already perfectly up-to-date!")
                elif status == "UPDATED":
                    messagebox.showinfo("MineSync", "Update successful! Your friends' data has been applied.")
                    self.refresh_timeline()
                elif status == "AHEAD":
                    messagebox.showinfo("MineSync", "You possess local unshared edits. Click on 'Share my world status'.")
                elif status == "CONFLICT_DETECTED":
                    self.ask_conflict_resolution()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.sync_btn.configure(text="🔄 Check if my world is up-to-date", state="normal")
        threading.Thread(target=run, daemon=True).start()

    def ask_conflict_resolution(self):
        """Explicit UI dialog interface handling multi-user parallel branch divergence"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚠️ Save Version Conflict Detected!")
        dialog.geometry("500x320")
        dialog.transient(self)
        dialog.grab_set()

        lbl = ctk.CTkLabel(dialog, text="Oops! Save Sync Conflict 🤯", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f5a623")
        lbl.pack(pady=15)

        txt = ("You and another player edited this world simultaneously offline.\n"
               "Which session version should become the master copy for the group?\n\n"
               "💡 Note: Your current local save was backed up into a separate safety branch.")
        lbl_txt = ctk.CTkLabel(dialog, text=txt, font=ctk.CTkFont(size=12), justify="center")
        lbl_txt.pack(pady=10, padx=20)

        def choose(option):
            self.git_manager.resolve_conflict(self.selected_world, option)
            dialog.destroy()
            messagebox.showinfo("Resolved", f"World synced and aligned with the chosen reference: {option}")
            self.refresh_timeline()

        btn_local = ctk.CTkButton(dialog, text="Keep MY Local Version (Overwrites Cloud)", fg_color="#e55353", hover_color="#c93b3b", command=lambda: choose("local"))
        btn_local.pack(fill="x", padx=40, pady=10, ipady=5)

        btn_remote = ctk.CTkButton(dialog, text="Keep the ONLINE Cloud Version (Overwrites Local Fles)", fg_color="#2eb85c", hover_color="#228a45", command=lambda: choose("remote"))
        btn_remote.pack(fill="x", padx=40, pady=5, ipady=5)

    def refresh_timeline(self):
        for widget in self.timeline_scroll.winfo_children():
            widget.destroy()
        commits = self.git_manager.get_timeline(self.selected_world)
        if not commits:
            ctk.CTkLabel(self.timeline_scroll, text="No save history tracking data found.").pack(pady=10)
            return

        if len(commits) > 1:
            reset_btn = ctk.CTkButton(self.timeline_scroll, text="💥 Rollback to very first version (Hard Reset)", fg_color="#df4759", hover_color="#b52b3a", command=lambda: self.trigger_rollback(commits[-1]["sha"]))
            reset_btn.pack(fill="x", padx=5, pady=5)

        for i, commit in enumerate(commits):
            card = ctk.CTkFrame(self.timeline_scroll, fg_color=("gray90", "gray25"))
            card.pack(fill="x", pady=4, padx=5)
            
            prefix = "⭐ Current Running Version" if i == 0 else f"📦 Saved Snapshot - {commit['date']}"
            lbl_title = ctk.CTkLabel(card, text=prefix, font=ctk.CTkFont(weight="bold", size=12))
            lbl_title.pack(anchor="w", padx=10, pady=2)

            if i > 0:
                rollback_btn = ctk.CTkButton(card, text="⏪ Restore", width=80, height=22, command=lambda s=commit["sha"]: self.trigger_rollback(s))
                rollback_btn.pack(anchor="e", padx=10, pady=5)

    def trigger_rollback(self, sha):
        if messagebox.askyesno("Rollback", "Restore this older version? Your current local adjustments will be replaced."):
            try:
                self.git_manager.rollback_to(self.selected_world, sha)
                messagebox.showinfo("Time Travel Success", "World version reverted! You can safely launch Minecraft now.")
                self.refresh_timeline()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def invite_friend(self):
        friend = self.collab_entry.get().strip()
        if not friend: return
        try:
            self.git_manager.invite_collaborator(self.selected_world, friend)
            messagebox.showinfo("Invited!", f"{friend} has been successfully granted repository access permissions.")
            self.collab_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Username could not be validated or API exception error: {e}")