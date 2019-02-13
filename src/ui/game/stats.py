import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from config import Config
from game import Game

import ui.game.game


class StatFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.create_title()
        self.create_point_widget()
        self.create_feed_widget()
        self.create_buttons()

    def create_title(self):
        """Create changing round number title at the top of the page.
        """
        font = tkFont.Font(**Config.ROUND_FONT)
        round_num_str = tk.StringVar()
        round_num_str.set(f"Round {self.parent.controller.game.round_num}")
        label2 = tk.Label(self, textvariable=round_num_str, font=font)
        label2.grid(row=0, column=0, columnspan=3, sticky="nsew")

    def create_point_widget(self):
        """Show player points during the game. The points update after
        every round.
        """
        font = tkFont.Font(**Config.POINT_FONT)
        point_frame = ttk.LabelFrame(self, text="Points")
        point_frame.grid(row=1, column=0, rowspan=2, padx=5, sticky="nsew")

        for i, player in enumerate(self.parent.controller.game.players):
            player_name = tk.StringVar()
            player_name.set(player.get_name())
            name_label = tk.Label(
                point_frame, textvariable=player_name, font=font)
            name_label.grid(row=i, column=0, sticky="w")

            points = tk.IntVar()
            points.set(player.get_points())
            point_label = tk.Label(point_frame, textvariable=points, font=font)
            point_label.grid(row=i, column=1, sticky="w", padx=10)

    def create_feed_widget(self):
        """Create the feed box that shows what happens during computers
        turns.
        """
        self.feed_frame = ttk.LabelFrame(self, text="Feed")
        self.feed_frame.grid(row=1, column=1, rowspan=2, padx=5, sticky="nsew")

        self.feed_frame.columnconfigure(0, weight=50)
        self.feed_frame.columnconfigure(1, weight=1)
        self.feed_frame.rowconfigure(0, weight=1)

        # scrollbar that activates when the feed box has
        # enough content
        self.vert_scroll = ttk.Scrollbar(self.feed_frame)
        self.vert_scroll.grid(row=0, column=1, sticky="nsw")

        self.feed_box = tk.Listbox(self.feed_frame,
                                   activestyle="dotbox",
                                   height=7,
                                   yscrollcommand=self.vert_scroll.set,
                                   highlightthickness=0)
        self.feed_box.grid(row=0, column=0, sticky="nsew")

        # set the scrollbar to control the feed boxes yview method
        self.vert_scroll["command"] = self.feed_box.yview

        # insert messages to the feed box
        for timestamp in self.controller.game.feed.messages:
            msg = " - ".join(timestamp)
            self.feed_box.insert(tk.END, msg)
            self.feed_box.yview(tk.END)

    def create_buttons(self):
        """Create next round, new game and quit buttons.
        """
        # create next round or new game buttons depending on
        # the state of the game
        if not self.controller.game.game_played:
            state = tk.NORMAL

            if not self.controller.game.round_played:
                state = tk.DISABLED

            round_button = ttk.Button(self,
                                      text="Next round",
                                      command=self.start_next_round,
                                      state=state)
            round_button.grid(row=1, column=2, sticky="ew")

        else:
            new_game_button = ttk.Button(self,
                                         text="New game",
                                         command=self.start_new_game)
            new_game_button.grid(row=1, column=2, sticky="ew")

        quit_button = ttk.Button(self,
                                 text="Quit",
                                 command=self.quit_game)
        quit_button.grid(row=2, column=2, sticky="ew")

    def start_next_round(self):
        self.controller.game.start_new_round()
        self.parent.update_stat_frame()
        self.parent.update_table_frame()
        self.parent.end_turn()

    def start_new_game(self):
        self.controller.game.start_new_game()
        self.controller.game_on = True
        self.parent.update_game_frame()

    def quit_game(self):
        self.controller.game = Game()
        self.controller.game_on = False
        self.controller.update_frames()
        self.controller.show_frame(ui.main_menu.MainScreen)

    def update_feed(self):
        self.feed_frame.destroy()
        self.create_feed_widget()
