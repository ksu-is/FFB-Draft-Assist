import requests
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox

CACHE_FILE = 'players_data.json'
CACHE_DATE_FILE = 'cache_date.txt'
