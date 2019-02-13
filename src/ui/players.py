import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import re

from config import Config

import ui.main_menu
import ui.game.game


class PlayerPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.padding = 10

        self.create_title()
        self.create_label_frame()
        self.create_player_widgets()
        self.create_buttons()

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="Players", font=font)
        title_label.grid(row=0, column=0, sticky="nsew")

    def create_label_frame(self):
        self.label_frame = ttk.LabelFrame(self, padding=10)
        self.label_frame.grid(row=1, column=0)

    def create_player_widgets(self):
        font = tkFont.Font(**Config.SETTING_FONT)
        self.player_widgets = []

        # entry validation method
        vcmd = (self.register(self.on_validate), '%P')

        # iterate over the player qty in order to create the correct
        # number of entry widgets
        for i in range(0, Config.PLAYER_QTY):
            label_text = "Player" if i == 0 else "Computer"
            player_name = tk.StringVar()
            player_label = tk.Label(self.label_frame,
                                    text=label_text,
                                    font=font)
            player_label.grid(row=i,
                              column=0,
                              sticky="nsw",
                              pady=self.padding,
                              padx=self.padding)

            player_entry = ttk.Entry(self.label_frame,
                                     textvariable=player_name,
                                     validate='key',
                                     validatecommand=vcmd,
                                     font=font)
            player_entry.grid(row=i,
                              column=1,
                              sticky="nsew",
                              pady=self.padding,
                              padx=self.padding)

            self.player_widgets.append((player_label, player_entry))

    def create_buttons(self):
        button_properties = {0: {"text": "Back",
                                 "command": lambda: self.controller.show_frame(ui.main_menu.MainScreen)},
                             1: {"text": "Play",
                                 "command": lambda: self.start(self.player_widgets)}}

        for column in button_properties:
            button = ttk.Button(self.label_frame, **button_properties[column])
            # row number 4 because the max number of players is 4. The buttons
            # will be positioned under the entry widgets.
            button.grid(row=4, column=column, sticky="nsew", padx=10)

    def on_validate(self, P):
        """Validates the player names in the entry widgets.
        The names can have only small or capital letters or numbers.
        Max length of the name is 15 chars.
        """
        pattern = re.compile(r"(^[a-zA-Z]{1,15}$|^Computer\s\d$)")
        match = pattern.match(P)
        return True if match else False

    def check_empty_entries(self, players):
        """If some of the entry widgets are left empty,
        this method will fill a default name in the field.

        :param players: A list of entry widgets
        """
        count = 1
        for label, player_entry in players:
            if len(player_entry.get()) < 1:
                if label.cget("text") == "Player":
                    player_entry.insert(0, "Player")
                else:
                    player_entry.insert(0, f"Computer {count}")
                    count += 1

    def start(self, players):
        """Start the game

        :param players: A list of entry widgets
        """
        self.check_empty_entries(players)

        # create player
        self.controller.game.create_player(players[0][1].get(), False)

        # create computers
        for _, computer in players[1:]:
            self.controller.game.create_player(computer.get(), True)

        self.controller.game.start_first_game()
        self.controller.game_on = True
        self.controller.show_frame(ui.game.game.GamePage)
