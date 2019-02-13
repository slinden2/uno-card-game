import tkinter as tk

from ui.help import HelpPage
from ui.game.game import GamePage
from ui.settings import SettingPage
from ui.players import PlayerPage
from ui.main_menu import MainScreen

from config import Config
from game import Game


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        """Controller class of the app.
        """
        super().__init__(*args, **kwargs)

        self.geometry("1024x768+16+100")
        self.resizable(width=False, height=False)
        self.iconbitmap(Config.ICON)

        tk.Tk.wm_title(self, "UNO Card Game")

        self.main_window = tk.Frame(self)
        self.main_window.pack(side="top", fill="both", expand=True)

        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)

        self.game = Game()
        self.game_on = False

        # controller dict
        self.frames = {}

        self.create_frames()
        self.show_frame(MainScreen)

    def create_frames(self):
        """Create frames and a controller dict.
        """
        for F in (MainScreen, PlayerPage, SettingPage, GamePage, HelpPage):
            frame = F(self.main_window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame):
        """Show a frame if found in controller dict.

        :param frame: Frame to be shown.
        """
        if frame in (PlayerPage, GamePage):
            # player and game frames must be updated before showing
            self.update_frame(frame)
        frame1 = self.frames[frame]
        frame1.tkraise()

    def update_frames(self):
        """Destroy all the frames and recreate them.
        """
        for frame in self.frames:
            self.frames[frame].destroy()
        self.create_frames()

    def update_frame(self, frame):
        """Destroy a frame and recreate it.
        """
        self.frames[frame].destroy()
        frame1 = frame(self.main_window, self)
        self.frames[frame] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")
