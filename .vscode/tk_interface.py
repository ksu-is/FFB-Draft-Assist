import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox
from player_data import get_players_data


class NFLPlayersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL Players Data")
        self.root.geometry("600x500")  # Window size

        # Player data container
        self.players_data = {}

        # Create a button to fetch player data
        self.button_fetch = tk.Button(self.root, text="Fetch NFL Players Data", command=self.fetch_players)
        self.button_fetch.pack(pady=10)

        # Create a search box (Entry widget)
        self.search_label = tk.Label(self.root, text="Search Player:")
        self.search_label.pack(pady=5)

        self.search_box = tk.Entry(self.root, width=50)
        self.search_box.pack(pady=5)
        self.search_box.bind("<KeyRelease>", self.filter_players)  # Bind the filter function

        # Create a Listbox to display player data
        self.players_listbox = Listbox(self.root, width=80, height=15)
        self.players_listbox.pack(pady=10)

        # Add a scrollbar to the listbox
        scrollbar = Scrollbar(self.players_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.players_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.players_listbox.yview)

        # Label to display player details
        self.details_label = tk.Label(self.root, text="", justify=tk.LEFT, anchor="w")
        self.details_label.pack(pady=10)

    def fetch_players(self):
        """Fetch and display player data."""
        self.players_data = get_players_data()  # Store data in the instance variable

        if self.players_data:
            print(f"Fetched or loaded {len(self.players_data)} players.")
            self.display_players(self.players_data)
        else:
            messagebox.showerror("Error", "Failed to load player data.")

    def display_players(self, players):
        """Display players in the listbox."""
        # Clear current listbox contents
        self.players_listbox.delete(0, tk.END)

        if isinstance(players, dict):
            # Iterate through players and add their names to the listbox
            for player_id, player_data in players.items():
                full_name = player_data.get('full_name', 'Unknown Player')
                position = player_data.get('position', 'Unknown Position')
                display_text = f"{full_name} ({position})"
                self.players_listbox.insert(tk.END, display_text)
        else:
            messagebox.showerror("Error", "Data format is incorrect.")

    def filter_players(self, event=None):
        """Filter the listbox based on search box input and show player details."""
        search_term = self.search_box.get().lower()

        # Clear current listbox contents before inserting filtered players
        self.players_listbox.delete(0, tk.END)

        matching_player = None  # Variable to hold the first matching player

        # Filter players based on search term
        for player_id, player_data in self.players_data.items():
            full_name = player_data.get('full_name', 'Unknown Player')
            position = player_data.get('position', 'Unknown Position')

            # Check if the search term matches part of the player's name (case insensitive)
            if search_term in full_name.lower():
                # Insert into the Listbox
                display_text = f"{full_name} ({position})"
                self.players_listbox.insert(tk.END, display_text)

                # Set the first matching player for displaying their details
                if not matching_player:
                    matching_player = player_data

        if matching_player:
            self.display_player_details(matching_player)  # Show details of the first match
        else:
            self.details_label.config(text="No matching player found.")

    def display_player_details(self, player_data):
        """Display detailed player information."""
        full_name = player_data.get('full_name', 'N/A')
        team = player_data.get('team', 'N/A')
        position = player_data.get('position', 'N/A')
        years_exp = player_data.get('years_exp', 'N/A')
        birth_date = player_data.get('birth_date', 'N/A')

        details_text = f"Full Name: {full_name}\n"
        details_text += f"Team: {team}\n"
        details_text += f"Position: {position}\n"
        details_text += f"Years of Experience: {years_exp}\n"
        details_text += f"Birth Date: {birth_date}"

        self.details_label.config(text=details_text)


# Create and start the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = NFLPlayersApp(root)
    root.mainloop()
