import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from config import Config

import ui.players
import ui.settings
import ui.help


class MainScreen(tk.Frame):

    def __init__(self, parent, controller):
        """Main menu
        """
        super().__init__(parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_logo()
        self.create_title()
        self.create_buttons()

    def set_logo(self):
        logo = tk.PhotoImage(file=Config.LOGO)
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo

        logo_label.grid(row=0, column=0)

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="CARD GAME", font=font)
        title_label.grid(row=1, column=0, sticky="ew")

    def create_buttons(self):
        # set up dict for button creation
        button_properties = {"Play": lambda: self.controller.show_frame(ui.players.PlayerPage),
                             "Settings": lambda: self.controller.show_frame(ui.settings.SettingPage),
                             "Help": lambda: self.controller.show_frame(ui.help.HelpPage),
                             "Quit": self.controller.quit}

        # create buttons
        for i, (text, command) in enumerate(button_properties.items(), start=2):
            button = ttk.Button(self,
                                text=text,
                                command=command,
                                width=30)
            button.grid(row=i, column=0, sticky="ns", pady=5)

            self.rowconfigure(i, weight=5)
