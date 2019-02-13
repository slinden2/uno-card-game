import tkinter as tk

from ui.game.stats import StatFrame
from ui.game.table import TableFrame


class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        """This class contains the actual game frame and all functionality
        that is linked to the game logic.
        """
        super().__init__(parent)
        self.controller = controller

        self.create_stat_frame()
        self.create_table_frame()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

    def create_stat_frame(self):
        """Stat frame is the frame that contains the feed and 
        the points of the players.
        """
        self.stat_frame = StatFrame(self, self.controller)
        self.stat_frame.grid(row=0, column=0, sticky="nsew")

    def create_table_frame(self):
        """Table refers to an actual table where the game 
        is to be played
        """
        self.table_frame = TableFrame(self, self.controller)
        self.table_frame.grid(row=1, column=0, sticky="nsew")

    def update_stat_frame(self):
        self.stat_frame.destroy()
        self.create_stat_frame()

    def update_table_frame(self):
        self.table_frame.destroy()
        self.create_table_frame()

    def update_game_frame(self):
        self.update_stat_frame()
        self.update_table_frame()

    def end_turn(self):
        """After every turn all the frames are updated
        so that the changes become visible to the user."""
        if self.controller.game.game_played:
            self.update_stat_frame()
            self.update_table_frame()
            self.controller.game_on = False

        elif (self.controller.game.turn_played_computer or
              self.controller.game.card_drawn or
              self.controller.game.round_played or
              self.controller.game.color_queried):
            self.update_table_frame()
            self.update_stat_frame()

        # while loop is needed for skipping the players
        # turn if more than one skip turn card is played
        while (self.controller.game.passing and not
               self.controller.game.round_played and not
               self.controller.game.color_queried):
            self.controller.game.pass_players_turn()
            self.update_table_frame()
            self.update_stat_frame()
