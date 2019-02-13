import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from config import Config

import ui.main_menu


class SettingPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)

        self.create_title()
        self.create_label_frame()
        self.create_setting_widgets()
        self.create_buttons()

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="Settings", font=font)
        title_label.grid(row=0, column=0, sticky="nsew")

    def create_label_frame(self):
        self.label_frame = ttk.LabelFrame(self, padding=10)
        self.label_frame.grid(row=1, column=0)

    def create_setting_widgets(self):
        # set up variables for setting labels and spinboxes
        font = tkFont.Font(**Config.SETTING_FONT)
        self.player_qty = tk.IntVar()
        self.player_qty.set(Config.PLAYER_QTY)
        self.winning_points = tk.IntVar()
        self.winning_points.set(Config.WINNING_POINTS)

        widget_properties = {"Player Quantity": {"increment": 1,
                                                 "from_": 2,
                                                 "to": 4,
                                                 "state": "readonly",
                                                 "wrap": True,
                                                 "textvariable": self.player_qty,
                                                 "width": 5},
                             "Winning Points": {"increment": 1,
                                                "from_": 20,
                                                "to": 500,
                                                "wrap": True,
                                                "textvariable": self.winning_points,
                                                "width": 5}}

        # create widgets
        for i, setting in enumerate(widget_properties):
            label = tk.Label(self.label_frame, text=setting, font=font)
            label.grid(row=i, column=0, sticky="e", padx=20)

            spinbox = tk.Spinbox(self.label_frame, **
                                 widget_properties[setting], font=font)
            spinbox.grid(row=i, column=1, sticky="w", padx=20)

    def create_buttons(self):
        button_properties = [{"text": "OK",
                              "command": self.save_settings},
                             {"text": "Cancel",
                              "command": self.undo_changes}]

        for i, kwargs in enumerate(button_properties):
            button = ttk.Button(self.label_frame, **kwargs, width=30)
            button.grid(row=i, column=2)

    def undo_changes(self):
        """Cancel all the changes and go back to main screen.
        """
        self.player_qty.set(Config.PLAYER_QTY)
        self.winning_points.set(Config.WINNING_POINTS)
        self.controller.show_frame(ui.main_menu.MainScreen)

    def save_settings(self):
        """Save changes and go back to main screen.
        """
        Config.PLAYER_QTY = self.player_qty.get()
        Config.WINNING_POINTS = self.winning_points.get()
        self.controller.update_frames()
        self.controller.show_frame(ui.main_menu.MainScreen)
