import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import webbrowser

from config import Config

import ui.main_menu


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        """Rules of the game
        """
        super().__init__(parent)

        self.controller = controller

        for i in range(0, 12):
            self.rowconfigure(i, weight=1)

        self.rowconfigure(12, weight=20)
        self.columnconfigure(0, weight=1)

        self.create_title()
        self.create_content()
        self.create_button()

    def create_title(self):
        """Title of the page
        """
        font = tkFont.Font(**Config.TITLE_FONT)

        label1 = ttk.Label(self, text="Help", font=font)
        label1.grid(row=0, column=0)

    def create_content(self):
        """Create content widgets
        """
        # set up title widge
        title_font = tkFont.Font(**Config.HELP_TITLE)
        title_label = tk.Label(self, text="Rules", font=title_font, padx=10)
        title_label.grid(row=1, column=0, sticky="w")

        # set up first paragraphs
        for i, paragraph in enumerate((Config.PARAGRAPH_1,
                                       Config.PARAGRAPH_2,
                                       Config.PARAGRAPH_3), start=2):
            content = tk.Message(self, text=paragraph, aspect=1500, padx=10)
            content.grid(row=i, column=0, sticky="w")

        # set up bullet points
        for i, bullet in enumerate((Config.BULLET_1,
                                    Config.BULLET_2,
                                    Config.BULLET_3), start=5):
            bullet = tk.Label(self, text=bullet)
            bullet.grid(row=i, column=0, sticky="w", padx=20)

        # set up last paragraphs
        for i, paragraph in enumerate((Config.PARAGRAPH_4,
                                       Config.PARAGRAPH_5), start=8):
            content = tk.Label(self, text=paragraph, padx=10)
            content.grid(row=i, column=0, sticky="w")

        # create a table
        table = HelpTable(self, Config.HELP_TABLE)
        table.grid(row=10, column=0, sticky="w", padx=20)

        # create a link to wikipedia source page
        link = tk.Label(self, text=Config.LINK_TEXT, cursor="hand2", padx=20)
        link.grid(row=11, column=0, sticky="w")
        link.bind("<Button-1>", self.open_webbrowser)

    def create_button(self):
        """"Back to MainScreen button
        """
        button = ttk.Button(self, text="Back",
                            command=self.back_to_mainscreen, width=30)
        button.grid(row=12, column=0)

    def back_to_mainscreen(self):
        self.controller.show_frame(ui.main_menu.MainScreen)

    @staticmethod
    def open_webbrowser(event):
        """Used for opening the Wikipedia source page
        """
        webbrowser.open(Config.HELP_LINK)


class HelpTable(tk.Frame):

    def __init__(self, parent, data):
        super().__init__(parent)
        self.borderwidth = 1
        self.data = data
        self.create_table()

    def create_table(self):
        title_font = tkFont.Font(**Config.HELP_TABLE_TITLE)
        for row_n, row_data in enumerate(self.data):
            for column_n, cell_data in enumerate(row_data):

                if row_n % 2 == 0:
                    # every other row with different bgcolor
                    frame = tk.Frame(self,
                                     borderwidth=1,
                                     background="#DADADA",
                                     relief="groove",
                                     padx=5)
                else:
                    frame = tk.Frame(self,
                                     borderwidth=1,
                                     relief="groove",
                                     padx=5)

                frame.grid(row=row_n, column=column_n, sticky="nsew")

                if row_n == 0:
                    # first row with bold font
                    message = tk.Message(frame,
                                         text=cell_data,
                                         aspect=500,
                                         font=title_font,
                                         background="#DADADA")
                elif row_n % 2 == 0:
                    # every other row with different bgcolor
                    message = tk.Message(frame,
                                         text=cell_data,
                                         aspect=500,
                                         background="#DADADA")
                else:
                    message = tk.Message(frame, text=cell_data, aspect=500)

                message.pack(side="left")
