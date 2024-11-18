import tkinter as tk
from tkinter import messagebox, Scrollbar
import tkinter.simpledialog as simpledialog
from player_data import get_players_data  # Assuming this function exists in a module


class NFLPlayersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL Players Data")
        self.root.geometry("1000x800")  # Window size (significantly larger)

        # Player data container
        self.players_data = {}

        # Search Debounce
        self.debounce_id = None

        # Create a button to fetch player data
        self.button_fetch = tk.Button(self.root, text="Fetch NFL Players Data", command=self.fetch_players)
        self.button_fetch.pack(pady=10)

        # Frame to hold filter buttons
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(pady=10)

        # Position Filter Button
        self.position_button = tk.Button(self.filter_frame, text="Filter by Position", command=self.filter_by_position)
        self.position_button.pack(side=tk.LEFT, padx=10)

        # Team Filter Button
        self.team_button = tk.Button(self.filter_frame, text="Filter by Team", command=self.filter_by_team)
        self.team_button.pack(side=tk.LEFT, padx=10)

        # Create a search box (Entry widget)
        self.search_label = tk.Label(self.root, text="Search Player:")
        self.search_label.pack(pady=5)

        self.search_box = tk.Entry(self.root, width=50)
        self.search_box.pack(pady=5)
        self.search_box.bind("<KeyRelease>", self.on_search)

        # Frame to hold the Listbox and Scrollbar
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a Listbox to display player data
        self.players_listbox = tk.Listbox(self.listbox_frame, width=80, height=20)  # Increased height
        self.players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the Listbox and place it on the right side
        self.scrollbar = Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.players_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.players_listbox.yview)

        # Label to display player details
        self.details_label = tk.Label(self.root, text="", justify=tk.LEFT, anchor="w", width=80)
        self.details_label.pack(pady=20)  # Increased padding for better separation

        # Bind a click event to the listbox to display player details
        self.players_listbox.bind('<<ListboxSelect>>', self.on_player_select)

    def fetch_players(self):
        """Fetch and display player data."""
        self.players_data = get_players_data()  # Store data in the instance variable

        if self.players_data:
            print(f"Fetched or loaded {len(self.players_data)} players.")
            self.display_players(self.players_data)
        else:
            messagebox.showerror("Error", "Failed to load player data.")

    def display_players(self, players):
        """Display players in the Listbox."""
        # Clear current listbox contents
        self.players_listbox.delete(0, tk.END)

        if isinstance(players, dict):
            # Iterate through players and add their names to the Listbox
            for player_id, player_data in players.items():
                if player_data is None:
                    continue  # Skip if player data is None

                full_name = player_data.get('full_name', 'Unknown Player')
                position = player_data.get('position', 'Unknown Position')
                display_text = f"{full_name} ({position})"
                self.players_listbox.insert(tk.END, display_text)
        else:
            messagebox.showerror("Error", "Data format is incorrect.")

    def on_search(self, event=None):
        """Handle search input and debounce the function."""
        if self.debounce_id:
            self.root.after_cancel(self.debounce_id)

        self.debounce_id = self.root.after(300, self.filter_players)

    def filter_players(self):
        """Filter the Listbox based on search box input."""
        search_term = self.search_box.get().strip().lower()

        if not search_term:
            self.display_players(self.players_data)  # Display all players if search term is empty
            return

        # Clear current Listbox contents before inserting filtered players
        self.players_listbox.delete(0, tk.END)

        # Filter players based on search term
        for player_id, player_data in self.players_data.items():
            if player_data is None:
                continue  # Skip if player data is None

            full_name = player_data.get('full_name', 'Unknown Player')
            position = player_data.get('position', 'Unknown Position')

            full_name = full_name.lower().strip()

            if search_term in full_name:  # This will match any part of the full name
                display_text = f"{full_name} ({position})"
                self.players_listbox.insert(tk.END, display_text)

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

    def on_player_select(self, event):
        """Handle the player selection from the Listbox."""
        selected_index = self.players_listbox.curselection()  # Get selected index
        if selected_index:
            selected_player_text = self.players_listbox.get(selected_index)
            selected_player_name = selected_player_text.split(" (")[0]  # Extract the player name from the text

            # Find the player data based on the selected player
            selected_player = None
            for player_id, player_data in self.players_data.items():
                if player_data and player_data.get('full_name', '').lower() == selected_player_name.lower():
                    selected_player = player_data
                    break

            if selected_player:
                self.display_player_details(selected_player)  # Show the details of the selected player

    def filter_by_position(self):
        """Filter the Listbox to show players of a specific position."""
        position = simpledialog.askstring("Filter by Position", "Enter the position (e.g. QB, WR):")
        if position:
            self.players_listbox.delete(0, tk.END)
            matching_player = None

            for player_id, player_data in self.players_data.items():
                if player_data is None:
                    continue  # Skip if player data is None

                # Safely get the position, default to empty string if None
                player_position = player_data.get('position', '').lower() if player_data.get('position') else ''

                if player_position == position.lower():
                    full_name = player_data.get('full_name', 'Unknown Player')
                    display_text = f"{full_name} ({position})"
                    self.players_listbox.insert(tk.END, display_text)

                    # Set the first matching player for displaying their details
                    if not matching_player:
                        matching_player = player_data

            if matching_player:
                self.display_player_details(matching_player)
            else:
                self.details_label.config(text="No players found for this position.")

    def filter_by_team(self):
        """Filter the Listbox to show players of a specific team."""
        team = simpledialog.askstring("Filter by Team", "Enter the team name:")
        if team:
            self.players_listbox.delete(0, tk.END)

            matching_player = None

            for player_id, player_data in self.players_data.items():
                if player_data is None:
                    continue  # Skip if player data is None

                player_team = player_data.get('team', '').lower() if player_data.get('team') else ''

                if player_team == team.lower():
                    full_name = player_data.get('full_name', 'Unknown Player')
                    display_text = f"{full_name} ({player_team})"
                    self.players_listbox.insert(tk.END, display_text)

                    if not matching_player:
                        matching_player = player_data

            if matching_player:
                self.display_player_details(matching_player)
            else:
                self.details_label.config(text="No players found for this team.")


# Create the Tkinter window instance
root = tk.Tk()

# Instantiate the NFLPlayersApp class
app = NFLPlayersApp(root)

# Run the Tkinter event loop
root.mainloop()
