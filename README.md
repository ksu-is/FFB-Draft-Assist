Overview
Project by Samuel Newlin
The FFB-Draft-Assist application is designed to help users in the process of a fantasy football draft by providing an interface to manage and display relevant player data. This tool is intended to streamline the decision-making process during a fantasy draft by presenting player statistics, draft positions, and projections in an easy-to-navigate format. The data used in the application is automatically fetched from the Sleeper Fantasy Football API, with caching implemented to reduce unnecessary API calls.
Features:

    Player Data: The application provides key statistics for each player including their:
        Full Name
        Team
        Position
        Average Draft Position (ADP)
        Projected Points per Week
        Projected Points per Season
    User Interface: A clean and simple interface where users can:
        Sort and filter players based on key attributes (e.g., team, position, ADP).
        View projected points to help with drafting decisions.
    Cache Management: The application automatically imports the player data once per day, minimizing unnecessary API traffic. The date of the last successful data fetch is saved to a cache_data.txt file.