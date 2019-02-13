import tkinter as tk
from tkinter import ttk


class QueryColorFrame(tk.Frame):

    def __init__(self, parent, controller):
        """Contains functionality related to choosing 
        the wild card color.
        """
        super().__init__(parent, width="10m")

        self.parent = parent
        self.controller = controller

        self.grid_propagate(0)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        if (self.controller.game.color_queried and
                self.controller.game.in_turn == 0):
            self.create_title()
            self.create_buttons()

    def create_title(self):
        label = ttk.Label(self, text="Choose a color")
        label.grid(row=0, column=0, columnspan=2)

    def create_buttons(self):
        button_grid_properties = {0: {"row": 1,
                                      "column": 0,
                                      "sticky": "nsew"},
                                  1: {"row": 1,
                                      "column": 1,
                                      "sticky": "nsew"},
                                  2: {"row": 2,
                                      "column": 0,
                                      "sticky": "nsew"},
                                  3: {"row": 2,
                                      "column": 1,
                                      "sticky": "nsew"}}

        for i, color in enumerate(self.controller.game.draw_deck.get_colors()):

            # translate command colors to actual colors supported by tcl
            button_color = {"red": "red",
                            "yel": "yellow",
                            "gre": "green",
                            "blu": "blue"}

            # lambda color=color stores the value of the color variable after
            # every iteration. If color=color is not defined, the value of the
            # color will be the same for every button. The value would be
            # the last value of the iteration.
            button = tk.Button(self,
                               background=button_color[color],
                               command=lambda color=color: self.process_color(color))
            button.grid(**button_grid_properties[i])

    def process_color(self, color):
        """Send the chosen wild card color to the game logic.
        """
        self.controller.game.receive_color(color)
        self.parent.parent.update_stat_frame()
        self.parent.parent.update_table_frame()
        self.parent.parent.end_turn()
