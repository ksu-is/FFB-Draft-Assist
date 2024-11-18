import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox
from player_data import get_players_data

class NFLPlayersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL Players Data")
        self.root.geometry("600x400")

        # Create a button to fetch player data
        self.button_fetch = tk.Button(self.root, text="Fetch NFL Players Data", command=self.fetch_players)
        self.button_fetch.pack(pady=10)

        # Create a Listbox to display player data
        self.players_listbox = Listbox(self.root, width=80, height=15)
        self.players_listbox.pack(pady=10)

        # Add a scrollbar to the listbox
        scrollbar = Scrollbar(self.players_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.players_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.players_listbox.yview)

    def fetch_players(self):
        """Fetch and display player data."""
        players = get_players_data()

        if players:
            self.display_players(players)
        else:
            messagebox.showerror("Error", "Failed to load player data.")

    def display_players(self, players):
        """Display players in the listbox."""
        # Clear current listbox contents
        self.players_listbox.delete(0, tk.END)

        # Check if players is a dictionary
        if isinstance(players, dict):
            # Iterate through players and add their names to the listbox
            for player_id, player_info in players.items():
                self.players_listbox.insert(tk.END, player_info['name'])